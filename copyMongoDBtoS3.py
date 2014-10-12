#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Backup MongoDB dumps to S3

Parameters
----------
None

Returns
-------
None

Long Description
"""

import boto
from boto.s3.key import Key
from datetime import date

s3 = boto.connect_s3()
# uses ~/.boto file for AWS keys

d = date.today()
today = d.isoformat()

# bucket -- cekeeper-mongodbbackup
# file = mongodb_backup.tar.gz
#


def move_to_S3():
    """Move mongodb backup to S3"""
    bucket = s3.get_bucket('cekeeper-mongodbbackup')
    key = Key(bucket)

    key.key = 'mongodb_dump_%s' % today
    key.set_contents_from_filename('/home/ubuntu/mongodb_backup.tgz')


def main():
    move_to_S3()


if __name__ == '__main__':
    main()

