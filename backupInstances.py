#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Form a complex number.

Keyword arguments:
real -- the real part (default 0.0)
imag -- the imaginary part (default 0.0)

"""

import sys
import boto
import traceback

ec2 = boto.connect_ec2()

# uses ~/.boto file for AWS keys

def backup():
    vols = {}

    print "Collecting running Instances\n"
    reservations = ec2.get_all_instances(filters={'instance-state-name': 'running'})
    instances = [i for r in reservations for i in r.instances]

    for instance in instances:
        volumes = ec2.get_all_volumes(filters={'attachment.instance-id' : instance.id})
        for volume in volumes:
            vols[volume] = (instance, volume.attach_data.device)

    for v in vols:
        print "Creating Snapshot of Volume: %s  Device: %s  Instance: %s" % (v, vols[v][1], vols[v][0])
        v.create_snapshot()

    print "Trimming snapshots"
    ec2.trim_snapshots(hourly_backups=8, daily_backups=7, weekly_backups=4)


def main():
    backup()

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e:
        raise e
    except SystemExit, e:
        raise e
    except Exception, e:
        print str(e)
        traceback.print_exc()
        sys.exit(1)
