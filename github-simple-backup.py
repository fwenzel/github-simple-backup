#!/usr/bin/env python
import os
from subprocess import call
import sys
import urllib
from xml.etree.ElementTree import ElementTree


# API URL to grab repository list
REPO_LIST_API = 'http://github.com/api/v2/xml/repos/show/%(username)s'
# github clone URL
CLONE_URL = 'git://github.com/%(username)s/%(repo_name)s.git'


def usage():
    print "Usage: ./github-simple-backup.py username /path/to/backup/\n"
    sys.exit()

def clone_or_pull(username, backup_dir, repo):
    repo_name = repo.find('name').text
    repo_desc = repo.find('description').text
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

    tree = ElementTree()
    tree.parse(urllib.urlopen(REPO_LIST_API % {'username': username}))
    repos = tree.findall('repository')
    for repo in sorted(repos, key=lambda x: x.find('name').text):
        clone_or_pull(username, backup_dir, repo)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main()
    else:
        usage()
