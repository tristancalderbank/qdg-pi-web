# QDG Pi Project
# Quantum Degenerate Gases Lab (Madison Research Group)
# graph-and-stat-table.js
# date: Jun 3, 2016
# author: tristan calderbank
# contact: tristan@alumni.ubc.ca
# purpose: performs setup of data recieving and server system on host computer
#          
from subprocess import call
import time
import os

def install_message(message):
    print ""
    print message
    print ""
    time.sleep(3)

username = raw_input("Enter linux username: ")
"""
# update packages
install_message("Updating packages via apt-get...")
call(["sudo", "apt-get", "update"])
call(["sudo", "apt-get", "upgrade"])

# install apache2 via apt-get
install_message("Installing apache2 via apt-get")
call(["sudo", "apt-get", "install", "apache2"])

# install python
install_message("Getting python via apt-get")
call(["sudo", "apt-get", "install", "python"])

# update pip, then use it to install redis-py
install_message("Updating pip via pip...")
call(["sudo", "pip", "install", "-U", "pip"])
install_message("Installing redis-py python module via pip...")
call(["sudo", "pip", "install", "redis"])

# download and compile redis
install_message("Downloading redis...")

operating_directory = "/home/" + username + "/Downloads/"
os.chdir(operating_directory)
redis_download_link = "http://download.redis.io/redis-stable.tar.gz"
call(["sudo", "wget", redis_download_link])
"""
install_message("Installing redis...")
#call(["sudo", "tar", "xvaf", "redis-stable.tar.gz"])
operating_directory = "/home/" + username + "/Downloads/" + "redis-stable"
os.chdir(operating_directory)
#call(["sudo", "make"])
#call(["sudo", "make", "test"])

call(["sudo", "killall", "redis-server"])
call(["sudo" , "cp", "src/redis-server", "/usr/local/bin/"])
call(["sudo", "cp", "src/redis-cli", "/usr/local/bin/"])
call(["sudo", "mkdir", "/etc/redis"])
call(["sudo", "mkdir", "/var/redis"])
call(["sudo", "cp", "utils/redis_init_script", "/etc/init.d/redis_6379"])

install_message("Cloning web files to /var/www/...")
operating_directory = "/home/var/www"
os.chdir(operating_directory)
call(["sudo", "git", "clone", "https://github.com/tristancalderbank/qdg-pi-web"])

call(["sudo", "cp", "/home/pi/qdg-pi/6379.conf", "/etc/redis/6379.conf"])

