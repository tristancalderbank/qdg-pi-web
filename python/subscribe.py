import sys
import os
import redis
import csv
import fcntl
import time

# configuration
master_table_IP = '10.1.137.162'
MOL_lab_IP = '10.1.137.203'
server_port = '6379'
server_ip = 'localhost'
max_number_of_sensors = 8
room_names = ["mol", "master"]


def connect_to_server(server_ip,server_port):
    r = redis.StrictRedis(host=server_ip, port=server_port, db=0)
    connected = False
    while connected == False:
        try:
            server_connection = redis.StrictRedis(host=server_ip, port=server_port, db=0)
            server_connection.ping()
            connected = True
            print "Successfully connected to redis-server at " + server_ip +"."
        except redis.exceptions.ConnectionError:
            print "Couldn't connect to redis server at " + server_ip + ", trying again in 5 seconds..."
            time.sleep(5)

    return server_connection

def check_if_connected(server_connection, server_ip, server_port):
    try:
        server_connection.ping()
        print "Still connected to server at " + server_ip + "." 
    except redis.exceptions.ConnectionError:
        print "Server at " + server_ip + " was disconnected, trying again..."
        server_connection = connect_to_server(server_ip, server_port)

    return server_connection


def get_message(pubsub):
    while True:
        message = pubsub.get_message()
        if (message is not None):
            return message
        time.sleep(1)

def parse_message(message):
    room = message['channel']
    message = message['data']
    exec('message = ' + message)
    timestamp = message[0]
    sensor_data = message[1:max_number_of_sensors + 1]
    return room, timestamp, sensor_data

 
def write_to_file(data_directory, room, timestamp, sensor_data):

    data_directory = data_directory + room
    file_name = timestamp[0:10] + ".csv"
    sensor_number = 0

    for sensor in sensor_data:
       
        if sensor != "no_data":
            sensor_directory = data_directory + "/" + "sensor_" + str(sensor_number) + "/"
            sensor_file_path = sensor_directory + file_name

            if not os.path.exists(sensor_directory):
                    os.makedirs(sensor_directory)




            data_file = open(sensor_file_path, "ab")
            fcntl.flock(data_file, fcntl.LOCK_EX)

            file_writer = csv.writer(data_file)
            file_writer.writerow([timestamp, sensor[0], sensor[1], sensor[2]]) 

            fcntl.flock(data_file, fcntl.LOCK_UN)
            data_file.close()



        sensor_number+=1

website_data_directory = "/var/www/qdg-pi-web/data/"

# main loop

while True:

    try:
        message = get_message(pubsub)
        room, timestamp, sensor_data = parse_message(message)
        write_to_file(website_data_directory, room, timestamp, sensor_data)
        print sensor_data
    except KeyboardInterrupt:
        raise
        exit()    
    except:
        server_connection = connect_to_server(server_ip, server_port)
        pubsub = server_connection.pubsub(ignore_subscribe_messages=True)
        for room in room_names:
            pubsub.subscribe(room)

    time.sleep(1)

