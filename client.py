import argparse
import csv
import socket
import e2d

parser = argparse.ArgumentParser(description="Client per l'avvio di una simulazione Energy2D  e l'acquisizione dei "
                                             "dati generati")
parser.add_argument("steps", type=int, help="Quantità di step da simulare")
parser.add_argument("steplength", type=int, help="Durata di uno step nella simulazione in secondi")
args = parser.parse_args()


thermostats = e2d.initialize_thermostats()  # inizializza il dizionario dei termostati
columns = e2d.initialize_data_columns(thermostats)  # inizializza l'array di colonne del csv con i dati

serverAddressPort = e2d.get_server_address_and_port()  # coppia indirizzo-porta del server
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # crea una socket UDP

csv_file = open(e2d.simulationDataFile, mode='w')  # apre il file csv per salvare i dati
writer = csv.DictWriter(csv_file, fieldnames=columns)
writer.writeheader()

e2d.send_message(UDPClientSocket, serverAddressPort, e2d.set_steplength_command(args.steplength))  # setta steplength
e2d.send_message(UDPClientSocket, serverAddressPort, e2d.reset_command())  # resetta la simulazione
e2d.send_message(UDPClientSocket, serverAddressPort, e2d.runsteps_command(100))  # esegue la simulazione per un secondo,
# tempo necessario affinché i termometri rilevino una temperatura valida
step = 100
while step < args.steps:  # ciclo principale che esegue la simulazione e raccoglie dati
    e2d.send_message(UDPClientSocket, serverAddressPort, e2d.runsteps_command(str(args.steplength)))

    fileRow = {"TIME": step}
    answer = e2d.send_message(UDPClientSocket, serverAddressPort, e2d.get_temperatures_command())
    temperatures = answer.split("   ")
    for t in temperatures:
        tSplit = t.split(" ")
        thermometerName = tSplit[0]
        if thermometerName.startswith(e2d.thermometerPrefix):
            temperature = tSplit[1]
            if thermometerName != "THERMOMETER_EXTERNAL":
                thermostats.get(thermometerName).update(UDPClientSocket, serverAddressPort, temperature, time=e2d.get_time(step, args.steplength))

                fileRow[thermometerName] = thermostats.get(thermometerName).temperature
                fileRow[e2d.get_heater_name(thermometerName)] = thermostats.get(thermometerName).heaterIsOn
            else:
                fileRow["THERMOMETER_EXTERNAL"] = temperature

    writer.writerow(fileRow)
    step += args.steplength
