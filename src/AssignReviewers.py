## @file
# Assign reviewers from .github/REVIEWERS using CODEOWNERS syntax
#
# Copyright (c) 2022, Intel Corporation. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
##

import os
import json
from   codeowners import CodeOwners
from   git        import Git
from   github     import Github

GitHubToken   = os.environ.get('INPUT_GITHUB_TOKEN')
GitHubPayload = json.loads(os.environ.get('GITHUB_CONTEXT'))

Hub = Github (GitHubToken)
print (Hub)

Hub = Github (GitHubPayload['token'])
print (Hub)

print (GitHubPayload['event']['action'])

print (GitHubPayload)

print (GitHubPayload['event']['action'])
