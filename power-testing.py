import matplotlib.pyplot as plt
import argparse
import csv
import socket
import e2d

parser = argparse.ArgumentParser(description="Client per l'avvio di una simulazione Energy2D  e l'acquisizione dei "
                                             "dati generati")
parser.add_argument("steps", type=int, help="Quantità di step da simulare")
args = parser.parse_args()

thermometers_name = e2d.get_thermometers_name_from_json()
columns = e2d.initialize_test_columns(thermometers_name)  # inizializza l'array di colonne del csv

serverAddressPort = e2d.get_server_address_and_port()  # coppia indirizzo-porta del server
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # crea una socket UDP

csv_file = open(e2d.testDataFile, mode='w')  # apre il file csv per salvare i dati
writer = csv.DictWriter(csv_file, fieldnames=columns)
writer.writeheader()

e2d.send_message(UDPClientSocket, serverAddressPort, e2d.reset_command())  # resetta la simulazione
steplength = 36
stepProgress = 100  # il file e2d di test ha steplength = 36s, quindi 100 step = 1h
e2d.send_message(UDPClientSocket, serverAddressPort, e2d.runsteps_command(stepProgress))

step = stepProgress
while step < args.steps:  # ciclo principale che esegue la simulazione e raccoglie dati
    e2d.send_message(UDPClientSocket, serverAddressPort, e2d.runsteps_command(str(stepProgress)))

    fileRow = {"TIME": step}
    answer = e2d.send_message(UDPClientSocket, serverAddressPort, e2d.get_temperatures_command())
    temperatures = answer.split("   ")
    for t in temperatures:
        tSplit = t.split(" ")
        thermometerName = tSplit[0]
        if thermometerName.startswith(e2d.thermometerPrefix):
            temperature = tSplit[1]
            fileRow[thermometerName] = temperature

    writer.writerow(fileRow)
    step += stepProgress
csv_file.close()


csv_file = open(e2d.testDataFile, mode='r')
time = []
temperatures = e2d.get_empty_list_of_lists(len(thermometers_name))
plots = csv.reader(csv_file, delimiter=',')
counter = 0
for row in plots:  # riempie le liste "time", "temperatures" e "heaters"
    counter += 1
    if (counter == 1) | ((counter % 2) == 0):  # salta le righe pari, sono vuote
        continue
    else:
        time.append(int(row[0]) / 100)
        i = 1
        while i < (len(thermometers_name) + 1):
            temperatures[i - 1].append(float(row[i]))
            i += 1

time.remove(time[0])
tempVariations = e2d.get_empty_list_of_lists(len(thermometers_name))
for i in range(len(thermometers_name)):
    j = 1
    while j < (len(temperatures[i])):
        tempVariations[i].append(temperatures[i][j] - temperatures[i][j - 1])
        j += 1

for i in range(len(thermometers_name)):
    plt.subplot(4, 4, i+1)
    plt.plot(time, tempVariations[i])
    plt.title(thermometers_name[i])

plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=None, hspace=0.35)

plt.show()
