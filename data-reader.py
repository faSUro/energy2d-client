import json
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
        i = 2
        while i < (len(thermometers_name) * 3):
            temperatures[int((i - 2) / 3)].append(float(row[i]))
            heaters[int((i - 2) / 3)].append(float(row[i + 1]))
            setpoints[int((i - 2) / 3)].append(float(row[i + 2]))
            i += 3

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
