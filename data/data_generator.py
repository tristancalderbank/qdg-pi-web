import random
import time
import datetime
import csv


start = 1284101485
sample_freq = 60
days = 365 * 2
samples = 86400 * days
progress = 0

timestamps = [start + offset for offset in range(0, samples, sample_freq)]

print len(timestamps)
for sensor in range(0,7):
    for element in timestamps:

        day = datetime.datetime.fromtimestamp(element).date()

        day = day.day

        progress += 1

        percent = float(progress) / float(len(timestamps)) * 100.0

        if(percent % 5 == 0):
            print("Progress: %f") % percent


        with open('mol/sensor_' + str(sensor) + "/" + str(datetime.datetime.fromtimestamp(element).date()) + '.csv', 'a') as current_file:

            current_file_csv = csv.writer(current_file)
            temperature = 22.3 + random.randint(-1000, 1000) / 100 + random.randint(-1,1) * day / 10
            pressure = 101325.4 + random.randint(-50000, 50000) / 100 + random.randint(-1,1) * day 
            humidity = 51.4 + random.randint(-500, 500) / 100 + random.randint(-1,1) * day / 10
            current_file_csv.writerow([datetime.datetime.fromtimestamp(int(element)).strftime('%Y-%m-%d %H:%M:%S'), temperature, pressure, humidity])

             








