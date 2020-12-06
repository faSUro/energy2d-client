# Energy2D Client

The client comes fully functional. In case you're not running Energy2D on the same machine of the client, you changed the port (8888 by default) or want to change the step progress (the number of steps between a sample and another), you'll need to edit the file _general-settings.json_, inside the _config_ folder.

### Initialize the client

While Energy2D is running, execute _init-thermostat.py_ to initialize the file _thermostat-settings.json_, inside the _config_ folder. This file will now contain a list of all the thermostats of the model currently open in Energy2D. For each thermostat there are two elements: its deadband and the weekly program. The program is composed by 7 numbers (from 0 to 6, corresponding to the days of the week, starting from Monday): each number is a dictionary with numbers from 0 to 23 (hours of the day) as keys and the programmed temperature (in Celsius degrees) as values. You can change the program as you prefer directly from the file.

### Start the simulation

Now that you've set the weekly program for the rooms of the condominium, you can start the simulation executing _client.py_. The scripts requests two arguments: the number of steps to simulate and the duration (in simulated seconds) of a single step. The data thus generated will be saved inside _data.csv_.
E.g.: If you start the script with the arguments 100800 and 6, you'll get a simulation of 100800 steps corresponding to 100800x6=604800 seconds or 7 weeks. _data.csv_ will contain 1008 rows, since the step progress in 100 (by default).

### Visualize the data

Finally, you can see the data produced by the simulation thanks to _data-reader.py_. In order to correctly show the data, the script requires two arguments: the number of rows and the number of graphs per row you want to see.
You'll see one graph for every apartment containing: the setpoint temperature for that apartment at any given time, the actual temperature, the external temperature and whether the heater is on or off (10 means on, 0 means off).
