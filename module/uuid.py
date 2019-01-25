#!/usr/bin/python
import platform
import subprocess

def get_uuid():
    if(platform.system() == 'Linux'):
        p = subprocess.Popen(['sudo dmidecode -t system | grep "UUID"'], shell = True, stdout=subprocess.PIPE)
        return (p.communicate()[0].strip().split(':'))[1].strip()
    elif(platform.system()== 'Windows'):
        p = subprocess.Popen(['wmic', 'csproduct', 'get','UUID','/format:value'], shell=True, stdout=subprocess.PIPE)
        return (p.communicate()[0].strip().split('='))[1].strip()
