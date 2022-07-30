## @file
# Assign reviewers from a REVIEWERS file using CODEOWNERS syntax
#
# Copyright (c) 2022, Intel Corporation. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
##

'''
AssignReviewers
'''
import os
import sys
import json
from   cached_property import cached_property
from   codeowners      import CodeOwners
from   git             import Repo
from   github          import Github

class AssignReviewers (object):
    def __init__ (self):
        self._Hub                = None
        self._HubPullRequest     = None
        self._EventContext       = None
        self._EmailToLogin       = {}
        self._InputToken         = os.environ.get('INPUT_TOKEN')
        self._EventPath          = os.environ.get('GITHUB_EVENT_PATH')
        self._EventName          = os.environ.get('GITHUB_EVENT_NAME')
        self._InputReviewersPath = os.environ.get('INPUT_REVIEWERS_PATH')
        self._repo               = None

    @cached_property
    def EventContext (self):
        # Verify that the event is a pull request
        if self._EventName not in ['pull_request', 'pull_request_target']:
            sys.exit(f"ERROR: Event({self._EventName}) must be 'pull_request' and 'pull_request_target'.")
        # Parse JSON file that contains the GitHub PR event context
        print(f"Parse JSON file GITHUB_EVENT_PATH:{self._EventPath}")
        try:
            self._EventContext = json.load(open(self._EventPath))
        except:
            sys.exit(f"ERROR: Unable to parse JSON file GITHUB_EVENT_PATH:{self._EventPath}")

        # Verify that all the JSON fields required to complete this action are present
        for Key in ['action', 'repository', 'pull_request']:
            if Key not in self._EventContext:
                sys.exit(f"ERROR: Event context does not contain '{Key}'")
        for Key in ['full_name']:
            if Key not in self._EventContext['repository']:
                sys.exit(f"ERROR: Event repository context does not contain '{Key}'")
        for Key in ['draft', 'commits', 'base', 'head', 'number', 'user', 'assignees', 'requested_reviewers', 'requested_teams']:
            if Key not in self._EventContext['pull_request']:
                sys.exit(f"ERROR: Event pull request context does not contain '{Key}'")
        if self._EventContext['pull_request']['draft']:
            # Exit with success if PR is a draft and do not assign reviewers
            sys.exit(0)
        for Key in ['repo', 'ref']:
            if Key not in self._EventContext['pull_request']['base']:
                sys.exit(f"ERROR: Event pull request base context does not contain '{Key}'")
        for Key in ['html_url']:
            if Key not in self._EventContext['pull_request']['base']['repo']:
                sys.exit(f"ERROR: Event pull request base repo context does not contain '{Key}'")
        for Key in ['sha']:
            if Key not in self._EventContext['pull_request']['head']:
                sys.exit(f"ERROR: Event pull request head context does not contain '{Key}'")
        for Key in ['login']:
            if Key not in self._EventContext['pull_request']['user']:
                sys.exit(f"ERROR: Event pull request user context does not contain '{Key}'")
        return self._EventContext

    @cached_property
    def EventRepository (self):
        return self.EventContext['repository']

    @cached_property
    def EventPullRequest (self):
        return self.EventContext['pull_request']

    @cached_property
    def EventCommits (self):
        return self.EventPullRequest['commits']

    @cached_property
    def EventBase (self):
        return self.EventPullRequest['base']

    @cached_property
    def EventHead (self):
        return self.EventPullRequest['head']

    @cached_property
    def Hub(self):
        # Use GitHub API to retrieve a Hub object using the input token
        print(f"Get Hub object using input token")
        try:
            self._Hub = Github (self._InputToken)
        except:
            sys.exit(f"ERROR: Unable to retrieve Hub object")
        return self._Hub

    @cached_property
    def HubPullRequest(self):
        # Use GitHub API to retrieve the pull request object
        print(f"Get HubPullRequest object for PR #{self.EventPullRequest['number']}")
        try:
            self._HubPullRequest = self.Hub.get_repo(self.EventRepository['full_name']).get_pull(self.EventPullRequest['number'])
        except:
            sys.exit(f"ERROR: Unable to retrieve PullRequest object")
        return self._HubPullRequest

    def CreateRepo(self, path, remote, url):
        # Initialize a new git repository and add a remote to the specified url
        try:
            print(f"Create repository for {url} in {path}")
            self._repo = Repo.init(path)
            self._repo.create_remote(remote, url = url)
        except:
            sys.exit(f"ERROR: Unable to create repository for {url} in {path}")
        return self._repo

    @cached_property
    def Repo(self):
        return self._repo

    def GetModifiedFiles(self, sha, commits):
        # Use git diff to determine the set of files modified by a set of commits
        print(f"Get files modified by commits in range {sha}~{commits}..{sha}")
        try:
            return self.Repo.git.diff(f"{sha}~{commits}..{sha}", '--name-only').split()
        except:
            sys.exit(f"ERROR: Unable to determine files modified in range {sha}~{commits}..{sha}")

    def _CodeOwnerPaths (self, BaseName, Override = ''):
        # Build prioritized list of file paths to search for a file with CODEOWNERS syntax
        return [Override, f'./{BaseName}', f'./docs/{BaseName}', f'./.github/{BaseName}']

    def _ParseCodeOwners (self, reference, paths):
        # Search prioritized list of paths for a CODEOWNERS syntax file and parse the first file found
        for file in paths:
            if file:
                print(f"Attempt to parse file {self.Repo.remote().name}/{reference}:{file}")
                try:
                    Result = CodeOwners(self.Repo.git.show(f"{self.Repo.remote().name}/{reference}:{file}"))
                    print(f"Found file {self.Repo.remote().name}/{reference}:{file}")
                    return Result
                except:
                    continue
        # No files found in the prioritized list
        return None

    def ParseCodeownersFile (self, reference):
        # Parse first CODEOWNERS file found in prioritized list
        return self._ParseCodeOwners (
                      reference,
                      self._CodeOwnerPaths('CODEOWNERS')
                      )

    def ParseReviewersFile (self, reference):
        # Parse first REVIEWERS file found in prioritized list
        return self._ParseCodeOwners (
                      reference,
                      self._CodeOwnerPaths('REVIEWERS', self._InputReviewersPath)
                      )

    def _LookupEmail (self, Email):
        # Check if email address has already been resolved to a GitHub ID
        if Email.lower() in self._EmailToLogin:
            return self._EmailToLogin[Email.lower()]
        # Use GitHub API search_users to search for the user by email address
        SearchResult = self.Hub.search_users(f"{Email} in:email")
        print (f"Search: {Email} {[x for x in SearchResult]}")
        # Cache and return the first GitHub ID associated with the email address
        for User in SearchResult:
            if Email.lower() == User.email.lower():
                self._EmailToLogin[Email.lower()] = User.login
                return User.login

    def GetCodeOwnerUsersAndTeams (self, ModifiedFiles, CodeOwners, Label):
        # Determine the full set of users and teams involved in the review of a
        # set of modified files
        FileCodeOwners = set()
        for File in ModifiedFiles:
            if CodeOwners:
                print (F"{Label} of {File}: {CodeOwners.of(File)}")
                FileCodeOwners |= set(CodeOwners.of(File))
            else:
                print (F"{Label} of {File}: []")
        # Convert the users and teams into sets of GitHub IDs
        UserCodeOwners = set()
        TeamCodeOwners = set()
        for Item in FileCodeOwners:
            if Item[0] == 'USERNAME':
                UserCodeOwners.add (Item[1][1:])
            elif Item[0] == 'TEAM':
                TeamCodeOwners.add (Item[1][1:])
            elif Item[0] == 'EMAIL':
                UserCodeOwners.add (self._LookupEmail (Item[1]))
        return UserCodeOwners, TeamCodeOwners

if __name__ == '__main__':
    # Initialize AssignReviewers object
    Request = AssignReviewers()

    # Create repository in localrepo directory and add remote to PR BASE with name origin
    Request.CreateRepo ('localrepo', 'origin', Request.EventBase['repo']['html_url'])

    # Fetch PR BASE with depth 1
    # This is required to read the CODEOWNERS and REVIEWERS files
    try:
        Request.Repo.remote().fetch(Request.EventBase['ref'], depth = 1)
    except:
        sys.exit(f"ERROR: Unable to fetch {Request.EventBase['ref']} with depth 1")

    # Fetch the set of PR commits in head sha to determine files modified by the PR
    # The commits from head sha are only used to perform a git diff operation to determine
    # the set of files modified by the PR.  This is the only potential use of files from
    # a fork.
    try:
        Request.Repo.remote().fetch(Request.EventHead['sha'], depth = Request.EventCommits + 1)
    except:
        sys.exit(f"ERROR: Unable to fetch {Request.EventHead['sha']} with depth {Request.EventCommits + 1}")

    # Get the list of files modified by this PR
    ModifiedFiles = Request.GetModifiedFiles(Request.EventHead['sha'], Request.EventCommits)

    # Determine the set of users and teams that are CODEOWNERS of the files modified by the PR
    UserCodeOwners, TeamCodeOwners = Request.GetCodeOwnerUsersAndTeams(ModifiedFiles, Request.ParseCodeownersFile(Request.EventBase['ref']), 'CODEOWNERS')

    # Determine the set of users and teams that are REVIEWERS of the files modified by the PR
    UserReviewers, TeamReviewers   = Request.GetCodeOwnerUsersAndTeams(ModifiedFiles, Request.ParseReviewersFile(Request.EventBase['ref']), 'REVIEWERS')

    # Add PR Author to set of PR assignees if Author is not already an assignee
    Author = Request.EventPullRequest['user']['login']
    CurrentAssignees = set([x['login'] for x in Request.EventPullRequest['assignees']])
    if Author not in CurrentAssignees:
        print (f"Add Assignee: {Author}")
        try:
            Request.HubPullRequest.add_to_assignees([Author])
        except:
            sys.exit(f"ERROR: Unable to add new assignee {Author}")

    # The PR author can never be a PR reviewer
    UserReviewers -= set([Author])

    # Get the current set of PR user and team reviewers
    CurrentUserReviewers = set([x['login'] for x in Request.EventPullRequest['requested_reviewers']])
    CurrentTeamReviewers = set([x['login'] for x in Request.EventPullRequest['requested_teams']])

    # Determine the set of user and team reviewers that need to be added to the PR
    # Remove users and teams that are already assigned to the PR as a reviewer
    # Remove users and teams that are CODEOWNERS.  GitHub adds CODEOWNERS.
    AddUserReviewers = (UserReviewers - CurrentUserReviewers) - UserCodeOwners
    AddTeamReviewers = (TeamReviewers - CurrentTeamReviewers) - TeamCodeOwners

    # Determine the set of user and team reviewers that need to be removed from the PR
    # Remove extra users and teams that are already assigned to the PR as a reviewer
    # but are not required based on the set of files modified.
    # Remove users and teams that are CODEOWNERS.  GitHub removes CODEOWNERS.
    #
    # NOTE: If extra reviewers are manually added to a PR that are not required based
    #       on the files modified by the PR, then these extra reviewers will be removed.
    RemoveUserReviewers = (CurrentUserReviewers - UserReviewers) - UserCodeOwners
    RemoveTeamReviewers = (CurrentTeamReviewers - TeamReviewers) - TeamCodeOwners

    # If any users or teams need to be added to the set of PR reviewers, then use GitHub API to add them
    if AddUserReviewers or AddTeamReviewers:
        print (f"Add Reviewers User: {AddUserReviewers} Team: {AddTeamReviewers}")
        Request.HubPullRequest.create_review_request(list(AddUserReviewers), list(AddTeamReviewers))

    # If any users or teams need to be removed from the set of PR reviewers, then use GitHub API to remove them
    if RemoveUserReviewers or RemoveTeamReviewers:
        print (f"Remove Reviewers User: {RemoveUserReviewers} Team: {RemoveTeamReviewers}")
        Request.HubPullRequest.delete_review_request(list(RemoveUserReviewers), list(RemoveTeamReviewers))
