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

REVIEWERS_PATHS = ['./REVIEWERS', './docs/REVIEWERS', './.github/REVIEWERS']

GitHubEventPayload = json.load(open(os.environ.get('GITHUB_EVENT_PATH')))
Hub = Github (os.environ.get ('INPUT_TOKEN'))
ReviewersPaths = [os.environ.get ('INPUT_REVIEWERS_PATH')] + REVIEWERS_PATHS
ReviewersPath = ''
for Path in ReviewersPaths:
    if Path and os.path.exists(Path):
        ReviewersPath = Path
print (Hub)
print (GitHubEventPayload['action'])
print (os.environ.get('GITHUB_RUN_ID'))
print (os.environ.get('GITHUB_RUN_NUMBER'))
print ('ReviewersPath:', ReviewersPath)
