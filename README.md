Python Backup
=============

This repository contains the source code to a Python script I wrote to perform backups of directories on my Ubuntu machine.    

This script is expected to be run by cron and on my machine, I run it with this command:    

```
   0 10 * * * /path/to/Development/workspace-python/PyWWW-Backup/main.py -d /path/to/Dropbox/www-backups -s /var/www 2>&1
```

### Backup and History Management    
Normally, for something like this it's usually advisable to maintain backups with timestamps [instead of overwriting as the case currently is].    
That's exactly why I'm using Dropbox [since Dropbox maintains the history of files uploaded -- up to a limit ;-)].    
