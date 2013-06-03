#!/usr/bin/env python
import json
import os
import re
import sys
import urllib
from subprocess import call


# API URL to grab repository list
REPO_LIST_API = 'https://api.github.com/users/%(username)s/repos?per_page=100'
# github clone URL
CLONE_URL = 'git://github.com/%(username)s/%(repo_name)s.git'
# "Next" link regex in API header.
NEXT_RE = re.compile(r'<([^>]+)>; rel="next"')


def usage():
    print "Usage: %s username /path/to/backup/" % sys.argv[0]
    sys.exit()

def clone_or_pull(username, backup_dir, repo):
    repo_name = repo['name']
    repo_desc = repo['description']
    print "Backing up %s..." % repo_name
    print "* %s" % repo_desc

    repo_dir = '/'.join([backup_dir, repo_name])
    if os.path.exists(repo_dir):
        call(['git', 'pull'], cwd=repo_dir)
    else:
        clone_url = CLONE_URL % {'username': username,
                                 'repo_name': repo_name}
        call(['git', 'clone', clone_url], cwd=backup_dir)
    print

def main():
    username = sys.argv[1]
    backup_dir = sys.argv[2]
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Paginate through repos.
    repos = []
    repo_url = REPO_LIST_API % {'username': username}
    while True:
        req = urllib.urlopen(repo_url)
        repos += json.load(req)

        # Next pagination link? If so, follow it.
        next_link = NEXT_RE.search(req.info().get('Link', ''))
        if next_link:
            repo_url = next_link.group(1)
            print repo_url
        else:
            break

    for repo in repos:
        clone_or_pull(username, backup_dir, repo)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main()
    else:
        usage()
