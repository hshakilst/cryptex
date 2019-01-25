#!/usr/bin/python
import subprocess

def query(statement):
    p = subprocess.Popen(['q -H -t -b "'+statement+'"'], shell=True, stdout=subprocess.PIPE)
    return p.communicate()[0].strip()

#query("select * from ./../database/courses.csv where courses like '%web tech%'")