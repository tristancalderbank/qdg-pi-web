import sys
import os
import redis
import csv

# configuration
server_port = '6379'
server_ip = 'localhost'
max_number_of_sensors = 8
room_names = ["mol", "master"]



def get_message(pubsub):
    while True:
        message = pubsub.get_message()
        if (message is not None):
            return message

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
            file_writer = csv.writer(data_file)
            file_writer.writerow([timestamp, sensor[0], sensor[1], sensor[2]]) 
            data_file.close()

        sensor_number+=1

website_data_directory = "/var/www/qdg-pi-web/data/"

server_connection = redis.StrictRedis(host=server_ip, port=server_port, db=0)

pubsub = server_connection.pubsub(ignore_subscribe_messages=True)

for room in room_names:
    pubsub.subscribe(room)

# main loop

while True:

    message = get_message(pubsub)
    room, timestamp, sensor_data = parse_message(message)
    print timestamp
    write_to_file(website_data_directory, room, timestamp, sensor_data)







