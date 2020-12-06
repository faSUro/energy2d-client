# Energy2D Client

The client comes fully functional. In case you're not running Energy2D on the same machine of the client, you changed the port (8888 by default) or want to change the step progress (the number of steps between a sample and another), you'll need to edit the file "general-settings.json", inside the "config" folder.

### Initialize the client

While Energy2D is running, execute "init-thermostat.py" to initialize the file "thermostat-settings.json", inside the "config" folder. This file will now contain a list of all the thermostats of the model currently open in Energy2D. For each thermostat there are two elements: its deadband and the weekly program. The program is composed by 7 numbers (from 0 to 6, corresponding to the days of the week, starting from Monday): each number is a dictionary with numbers from 0 to 23 (hours of the day) as keys and the programmed temperature (in Celsius degrees) as values. You can change the program as you prefer directly from the file.

### Start the simulation

Now that you've set the weekly program for the rooms of the condominium, you can start the simulation executing "client.py". The scripts requests two arguments: the number of steps to simulate and the duration (in simulated seconds) of a single step. The data thus generated will be saved inside "data.csv".
E.g.: If you start the script with the arguments 100800 and 6, you'll get a simulation of 100800 steps corresponding to 100800x6=604800 seconds or 7 weeks. "data.csv" will contain 1008 rows, since the step progress in 100 (by default).

### Visualize the data

Finally, you can see the data produced by the simulation thanks to "data-reader.py". In order to correctly show the data, the script requires one argument: the total amount of apartments inside the building.
