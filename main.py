#!/usr/bin/env python3
import glob
import os
import os.path
import sys
'''
This script basically performs the function of backing up folders.

It's provided with a destination directory (i.e. the folder where backups will be saved) and a 
source directory (i.e.where folders should be read and backed up).
It iteratively takes each folder, compresses it and moves the compressed file to the destination 
directory.

NOTE: It only backs up folders, not files

@author: eokeke<emmanix2002@gmail.com>
'''
__version__ = "1.2"
str_usage_help = """\
    USAGE: main.py [arguments]
    -h                   Show this help message
    -s source_dir        Specify the source directory for the backup
    -d destination_dir    Specify the destination directory for the backup
"""
arguments = {'source':'','destination':''}
"""
Displays the help message to the user
"""
def show_help():
    print(str_usage_help)
"""
Sets the default values for appropriate indexes
"""
def set_defaults():
    arguments['destination'] = os.path.join(os.environ['HOME'],"backup")
"""
Checks and decides if processing should continue or it should exit at this point
@param print_error_message: A boolean that determines if to print a message describing the error 
"""
def check_status(print_error_message=True):
    errors = []
    keys = ['source','destination']
    try:
        for key in keys:
            if(len(arguments[key]) == 0):
                errors.append("A string of length zero (0) was specified as the {0} path".format(key))
                raise Exception('A string of length zero (0) was specified as the {0} path'.format(key))
                if(not os.path.exists(arguments[key])):
                    errors.append("The {0} path {1} does not exist".format(key,arguments[key]))
                    raise Exception('The {0} path does not exist'.format(key))
                    if(not os.path.isdir(arguments[key])):
                        #not a directory
                        errors.append("The {0} path {1} does not seem to be a valid directory".format(key,arguments[key]))
                        raise Exception('The {0} path does not seem to be a valid directory'.format(key))
    except Exception as exception:        
        if(print_error_message):
            print(errors)
        raise exception
"""
Handles the entire backup process from start to finish
@param verbose: boolean that specifies that the program should be verbose 
"""
def do_backup(verbose=True):
    paths = glob.glob(os.path.join(arguments['source'],"*"))
    directories = [path for path in paths if(os.path.isdir(path))]
    #filter out everything else except directories
    base_tar_command = "tar -cf {0} {1}"
    if verbose:
        print("Using base command : {0}".format(base_tar_command))
    #the command format
    archives = []
    #list to hold the set of created archives
    for directory in directories:
        if verbose:
            print("Processing directory: {0}".format(directory))
        dir_base_name = os.path.basename(directory)
        dir_parent_name = os.path.dirname(directory)
        archive_name = os.path.join(dir_parent_name,dir_base_name+".tar")
        tar_command = base_tar_command.format(archive_name,directory)
        if verbose:
            print("Tar command: {0}".format(tar_command))
        if(os.system(tar_command) == 0):
            #it was successful
            if verbose:
                print("Compression successful")
            archives.append(archive_name)
        else:
            print('Failed to create archive {0}'.format(archive_name))
    if(len(archives) > 0):
        #archives were created
        if verbose:
            print("Preparing to move files")
        for archive in archives:
            if verbose:
                print("Moving archive: {0}".format(archive))
            archive_base_name = os.path.basename(archive)
            backup_archive_path = os.path.join(arguments['destination'],archive_base_name)
            if verbose:
                print("Moving to: {0}".format(backup_archive_path))
            os.rename(archive, backup_archive_path)

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        #means no arguments were supplied
        show_help()
    else:
        #means we have some command line arguments
        if(sys.argv[1].lower() == '-h'):
            #show help message
            show_help()
        else:
            arg_count = len(sys.argv)
            item_key = ""
            for i in range(1,arg_count,2):
                if(sys.argv[i].lower() == "-s"):
                    #dealing with the source directory
                    item_key = "source"
                elif(sys.argv[i].lower() == "-d"):
                    #dealing with the destination
                    item_key = "destination"
                if(i+1 < arg_count):
                    #only do this if the number of items in the argument list is long enough
                    arguments[item_key] = sys.argv[i+1]
            try:
                check_status()
                do_backup()
            except Exception as exception:
                message = exception.args
                print("Exception: {0}".format(message))
                sys.exit(1)