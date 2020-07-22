import json
import os
import matplotlib.pyplot as plt
import csv
import e2d

thermometers_name = e2d.get_thermometers_name_from_json()
time = []
# ext_temperature = []
temperatures = e2d.get_empty_list_of_lists(len(thermometers_name))
heaters = e2d.get_empty_list_of_lists(len(thermometers_name))
setpoints = e2d.get_empty_list_of_lists(len(thermometers_name))

csv_file = open(e2d.simulationDataFile, 'r')
plots = csv.reader(csv_file, delimiter=',')
counter = 0
for row in plots:  # riempie le liste "time", "temperatures" e "heaters"
    counter += 1
    if (counter == 1) | ((counter % 2) == 0):  # salta le righe pari, sono vuote
        continue
    else:
        time.append(int(row[0]))
        # ext_temperature.append(float(row[1]))
        for i in range(len(thermometers_name)+1):
            if i == 0:  # salta la prima colonna che corrisponde al tempo
                continue
            else:
                temperatures[i - 1].append(float(row[i * 2]))
                heaters[i - 1].append(float(row[((i * 2) + 1)]))


data = json.load(open(e2d.thermostatSettingsFile))
j = 0
for tm in thermometers_name:  # riempie la lista dei setpoint
    for i in range(len(time)):
        setpoints[j].append(int(data.get(tm).get("setpoint")))
    j += 1

for i in range(len(thermometers_name)):
    plt.subplot(4, 4, i+1)
    plt.plot(time, temperatures[i], label='int')
    # plt.plot(time, ext_temperature, '--', label='ext')
    plt.plot(time, heaters[i], label='O/I')
    plt.plot(time, setpoints[i], '--', label='sp')
    plt.title(thermometers_name[i])
    plt.legend(fontsize=8)

plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=None, hspace=0.35)

plt.show()
