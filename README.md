# qdg-pi-web
Serves temperature, pressure, and humidity data collected by up to 16 sensors using two Raspberry Pi's. Data is recieved via a redis database server and plotted using Highcharts javascript library.


###Instructions:

Navigate to /var/www/ and clone the repo in that directory. Run server-setup.py with sudo priviledges to install required software. Make sure that on each Raspberry Pi, the ip address in the script "publish-data.py" points to the computer that is hosting the page.

####Note:
This setup script will install the following dependencies: lighttpd, redis, redis-py

It then installs configuration files for redis and lighttpd, and sets up cronjobs for starting redis and the python subscribe script upon reboot.

If these changes sound like they will conflict with something already running on the computer, I would advise you to read through the server-setup.py script before running it.

###How it works:

1) The computer which recieves the data from the Raspberry Pis hosts a database server called "redis" which allows a "pubsub" system to be created. A python module called "redis-py" allows all the scripting of this database to be written in python. 

2) The two pis connect to the server and publish their sensor data to two channels: mol and master. 

3) The host computer can then subscribe to these channels and save the data into csv files located in the web server directory, this is the job of "subscribe.py"

4) The host computer also serves a webpage for viewing the data, using a lightweight server called "lighttpd"

5) Each button on the page tells the server to run a data processing script which processes the raw data, calculates stats, and generates the actual data to be displayed on the page, this is all done by passing different parameters to the script "process-data.py"


