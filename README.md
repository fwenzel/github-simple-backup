github-simple-backup
====================

I needed a simple backup solution for github, that just goes ahead and clones
all my public repositories (I don't have any other ones anyway). So here you
go.

Requirements
------------
* Python 2.6
* git

Usage
-----
    ./github-simple-backup.py github_username path/to/backup-dir

License
-------
github-simple-backup is licensed under the New BSD License. Check the file
LICENSE for more information.

Contributors
------------
* Frédéric Wenzel (Original Author)
* Jeff Balogh

Known Issues
------------
* The backup script does not handle the removal of repositories yet, since I
  don't think I've ever removed one before. Patches are welcome though!

