#!/usr/bin/env python

import sys
import shlex
import time
from subprocess import PIPE, Popen

def run(cmd):
    p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if stdout:
        sys.stdout.write("[stdout]:")
        sys.stdout.write(stdout)
    if stderr:
        sys.stdout.write("[stderr]:")
        sys.stdout.write(stderr)
    return stdout, stderr

conf = """
[program:mcstatus_node]
command=mcstatus_node
directory=/
process_name=mcstatus_node
user=nobody
group=nogroup
stdout_logfile=/tmp/mcstatus_stdout.log
stdout_logfile_maxbytes=2MB
stdout_logfile_backups=5
stdout_capture_maxbytes=2MB
stdout_events_enabled=false
stderr_logfile=/tmp/mcstatus_stderr.log
stderr_logfile_maxbytes=2MB
stderr_logfile_backups=5
stderr_capture_maxbytes=2MB
stderr_events_enabled=false
"""

def main():
    run("apt-get install -y python python-pip supervisor")
    run("pip install bottle")
    with open("/etc/supervisor/conf.d/mcstatus.conf", "w") as f:
        f.write(conf)
    run("supervisorctl reread")
    run("supervisorctl update")
    time.sleep(1000)
    run("supervisorctl status")

if __name__ == "__main__":
    main()
