import json
import e2d
import socket

serverAddressPort = e2d.get_server_address_and_port()  # coppia indirizzo-porta del server
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # crea una socket UDP

thermometers = e2d.get_thermometers_name_from_server(UDPClientSocket, serverAddressPort)  # ottiene la lista dei termometri
thermostats = e2d.build_default_thermostat_dict(thermometers)  # costruisce il dizionario dei termostati standard
# (setpoint = 20.0 e deadband = 0.5)

json_file = open(e2d.thermostatSettingsFile, 'w')
json.dump(thermostats, json_file, indent=2)  # scrive il dizionario dei termostati nel file json apposito
