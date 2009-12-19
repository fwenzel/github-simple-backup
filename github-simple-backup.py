#!/usr/bin/env python
import json
import os
from subprocess import call
import sys
import urllib


# API URL to grab repository list
REPO_LIST_API = 'http://github.com/api/v2/json/repos/show/%(username)s'
# github clone URL
CLONE_URL = 'git://github.com/%(username)s/%(repo_name)s.git'


def usage():
    print "Usage: ./github-simple-backup.py username /path/to/backup/\n"
    sys.exit()

def clone_or_pull(username, backup_dir, repo):
    print "Backing up %s..." % repo['name']
    print "* %s" % repo['description']
    repo_dir = '/'.join([backup_dir, repo['name']])
    if os.path.exists(repo_dir):
        call(['git', 'pull'], cwd=repo_dir)
    else:
        clone_url = CLONE_URL % {'username': username,
                                 'repo_name': repo['name']}
        call(['git', 'clone', clone_url], cwd=backup_dir)
    print

def main():
    username = sys.argv[1]
    backup_dir = sys.argv[2]
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    j = json.load(urllib.urlopen(REPO_LIST_API % {'username': username}))
    repos = j['repositories']
    for repo in sorted(repos, key=lambda x: x['name']):
        clone_or_pull(username, backup_dir, repo)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main()
    else:
        usage()
