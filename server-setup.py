# QDG Pi Project
# Quantum Degenerate Gases Lab (Madison Research Group)
# server-setup.py
# date: Jun 3, 2016
# author: tristan calderbank
# contact: tristan@alumni.ubc.ca
# purpose: performs setup of data recieving and server system on host computer
#
from subprocess import call
from subprocess import Popen
import time
import os

def install_message(message):
    print ""
    print message
    print ""
    time.sleep(3)

username = raw_input("Enter linux username: ")

# update packages
install_message("Updating packages via apt-get...")
call(["sudo", "apt-get", "update"])
call(["sudo", "apt-get", "upgrade"])

# install lighttpd web server
install_message("Installing lighttpd web server via apt-get")
call(["sudo", "apt-get", "install", "lighttpd"])

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
install_message("Installing redis...")
call(["sudo", "tar", "xvaf", "redis-stable.tar.gz"])
operating_directory = "/home/" + username + "/Downloads/" + "redis-stable"
os.chdir(operating_directory)
call(["sudo", "make"])
call(["sudo", "make", "test"])

call(["sudo", "killall", "redis-server"])
call(["sudo" , "cp", "src/redis-server", "/usr/local/bin/"])
call(["sudo", "cp", "src/redis-cli", "/usr/local/bin/"])
call(["sudo", "mkdir", "/etc/redis"])
call(["sudo", "mkdir", "/var/redis"])
call(["sudo", "cp", "utils/redis_init_script", "/etc/init.d/redis_6379"])

# Redis / Apache config
install_message("Configuring redis and lighttpd...")
call(["sudo", "cp", "/var/www/qdg-pi-web/config/6379.conf", "/etc/redis/6379.conf"])
install_message("Backing up current apache configuration...")
call(["sudo", "mv", "/etc/lighttpd/lighttpd.conf", "/etc/lighttpd/lighttpd-backup.conf"])
install_message("Installing qdg-pi config for lighttpd...")
call(["sudo", "cp", "/var/www/qdg-pi-web/config/lighttpd.conf", "/etc/lighttpd"])

install_message("Adding lighttpd user as owner of data and python folders in web directory...")
call(["sudo", "chown", "-R", "www-data", "/var/www/qdg-pi-web/python"])
call(["sudo", "chown", "-R", "www-data", "/var/www/qdg-pi-web/data"])

# Cronjobs
install_message("Setting up python subscribe script and redis as cronjobs...")
call(["sudo", "cp", "/var/www/qdg-pi-web/config/qdg-pi-cron", "/etc/cron.d/qdg-pi-cron"])
install_message("Restarting apache server...")
call(["sudo", "service", "apache2", "restart"])
install_message("Starting redis-server...")
call(["sudo", "redis-server", "/etc/redis/6379.conf"])
install_message("Starting python subscribe script...")
Popen(["sudo", "python", "/var/www/qdg-pi-web/python/subscribe.py"])
install_message("Done.")


















