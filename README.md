Simple flight tracking system

### Technologies used:
	-Mondial database
	-PostGIS library
	-PostgreSQL
	
### Main functionalities:
	-flight(id, airport) adds new flight to database
	-list_flights(id) lists all intersecting flights in database
	-list_cities(id, dist) lists cities lying closer than "dist" to any flight in database 
	
### How to run it?

In the PostgreSQL database there has to be city and airport table(tables from Mondial database).
In addition to that there has to be user named **"app"** with permission to access database **"student"**
with password **"qwerty"**. PostgreSQL database has to be set up for working with Postgis.

To work with PostgreSQL in Python I installed **psycopg2-binary** extension.

When running program for the first time use **"python3 program.py --init"** command.
After first initialisation **"python3 program.py"** command will be enough.

In order to exit program press **"ctr + c"**.




