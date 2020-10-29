# Energy2D Client

The client comes fully functional. In case you're not running Energy2D on the same machine of the client, you changed the port (8888 by default) or want to change the step progress (the number of steps between a sample and another), you'll need to edit the file "general-settings.json", inside the "config" folder.

### Initialize the client

While Energy2D is running, execute "init-thermostat.py" to initialize the file "thermostat-settings.json", inside the "config" folder. This file will now contain a list of all the thermostat of the model currently open in Energy2D. For each thermostats there are two elements: its deadband and the weekly program. The program is composed by 7 numbers (from 0 to 6, corresponding to the days of the week, starting from Monday): each number is a dictionary with numbers from 0 to 23 (hours of the day) as keys and the programmed temperature (in Celsius degrees) as values. You can change the program as you prefer directly from the file.

### Execute "client.py" while Energy2D is running to start the simulation and collect data to fill "data.csv"

### Execute "data-reader.py" to view the data produced
