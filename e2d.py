import json
import os

thermometerPrefix = "THERMOMETER"
heaterPrefix = "HEATER"
setpointPrefix = "SETPOINT"

thermostatSettingsFile = os.getcwd() + "/config/thermostat-settings.json"
generalSettingsFile = os.getcwd() + "/config/general-settings.json"
simulationDataFile = os.getcwd() + "/simulation_data/data.csv"
testDataFile = os.getcwd() + "/simulation_data/test-data.csv"


def set_heater_power_command(heater, power):
    return "set " + heater + ".power " + str(power)


def set_steplength_command(steplength):
    return "set timestep " + str(steplength)


def reset_command():
    return "reset"


def run_command(n):
    return "run " + str(n)


def get_temperatures_command():
    return "get allthermometers.temperature"


def runsteps_command(n):
    return "runsteps " + str(n)


def send_message(client_socket, server_address_port, message):
    req = str.encode(message)
    client_socket.sendto(req, server_address_port)  # sends to server using created UDP socket

    buffer_size = 4194304  # 4MB
    resp = client_socket.recvfrom(buffer_size)
    return str(resp[0], 'utf-8')  # ritorna la risposta del server decodificata


def get_heater_name(thermometer):  # metodo che ritorna il nome del termosifone a partire dal nome del termometro
    heater = heaterPrefix + thermometer[11:]
    return heater


def get_setpoint_name(thermometer):  # metodo che ritorna il nome del setpoint a partire dal nome del termometro
    setpoint = setpointPrefix + thermometer[11:]
    return setpoint


def initialize_data_columns(thermostats):
    columns = ["TIME", "THERMOMETER_EXTERNAL"]
    for ts in thermostats:  # riempie la lista contenente le colonne con i nomi dei termometri,
        # dei termosifoni e dei setpoint
        columns.append(thermostats.get(ts).thermometerName)
        columns.append(thermostats.get(ts).heaterName)
        columns.append(thermostats.get(ts).setpointName)
    return columns


def initialize_test_columns(thermometers):
    columns = ["TIME"]
    for ts in thermometers:  # riempie la lista contenente le colonne con i nomi dei termometri
        columns.append(ts)
    return columns


secondsInAMinute = 60
minutesInAnHour = 60
hoursInADay = 24
daysInAWeek = 7


def get_time(step, steplength):
    seconds_from_start = step * steplength
    minutes_from_start = seconds_from_start / secondsInAMinute
    hours_from_start = int(minutes_from_start / minutesInAnHour)
    days_from_start = int(hours_from_start / hoursInADay)

    day = days_from_start % daysInAWeek
    hour = hours_from_start % hoursInADay

    time = (day, hour)
    return time


class Thermostat:  # classe che rappresenta il termostato
    def __init__(self, thermometer_name, deadband, program):
        self.thermometerName = thermometer_name
        self.temperature = 0.0
        self.program = program
        self.deadband = float(deadband)
        self.setpointName = get_setpoint_name(thermometer_name)
        self.setpoint = 20.0
        self.heaterName = get_heater_name(thermometer_name)
        self.heaterIsOn = 0

    def update_setpoint(self, time):  # imposta il setpoint in base al giorno e all'ora
        self.setpoint = self.program[str(time[0])][str(time[1])]
        # time[0] = giorno, time[1] = ora

    def update(self, clientsocket, server_address_port, temp, time):
        self.update_setpoint(time)
        self.temperature = float(temp)
        message = "none"
        if (self.setpoint - self.temperature) > self.deadband:  # se la temperatura è troppo bassa
            message = set_heater_power_command(self.heaterName, power=100)  # comando che accende il termosifone
            self.heaterIsOn = 10
        elif (self.temperature - self.setpoint) > self.deadband:  # se la temperatura è troppo alta
            message = set_heater_power_command(self.heaterName, power=0)  # comando che spegne il termosifone
            self.heaterIsOn = 0
        send_message(clientsocket, server_address_port, message)


def get_thermometers_name_from_json():
    data = json.load(open(thermostatSettingsFile))  # apre il file di configurazione dei termostati
    return list(data.keys())


def initialize_thermostats():
    data = json.load(open(thermostatSettingsFile))
    thermometers_name = list(data.keys())
    thermostats = {}
    for tm in thermometers_name:
        thermostats[tm] = Thermostat(tm, data.get(tm).get("deadband"), data.get(tm).get("program"))
    return thermostats


def get_thermometers_name_from_server(client_socket, server_address_port):
    thermometers = []
    answer = send_message(client_socket, server_address_port, get_temperatures_command())
    split_answer = answer.split("   ")
    for t in split_answer:
        split = t.split(" ")
        thermometer_name = split[0]
        if (thermometer_name.startswith(thermometerPrefix)) & (thermometer_name != "THERMOMETER_EXTERNAL"):
            thermometers.append(thermometer_name)

    return thermometers


def build_default_thermostat_dict(thermometers):
    thermostats = {}
    week_program = {}
    day_program = {}

    for h in range(hoursInADay):
        day_program[h] = 20.0

    for d in range(daysInAWeek):
        week_program[d] = day_program

    for t in thermometers:
        thermostats[t] = {
            "deadband": 0.5,
            "program": week_program
        }
    return thermostats


def get_server_address_and_port():
    settings_file = json.load(open(generalSettingsFile))
    address_port = (settings_file.get("server_address"), settings_file.get("server_port"))
    return address_port


def get_empty_list_of_lists(size):
    list_of_lists = []
    for i in range(size):
        list_of_lists.append([])
    return list_of_lists


def get_step_progress():
    settings_file = json.load(open(generalSettingsFile))
    step_progress = settings_file.get("step_progress")
    return step_progress
