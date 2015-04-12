####################################
      HOW TO RUN APPLICATION
####################################
Requirements:
1. Python 2.7.6 with Standard Library
2. psycopg2 packet from python library
3. PostgreSQL database version 9+

FILES IN PACKAGE:
tournament.py -- implementation of a tournament
tournament.sql -- table definitions for the tournament project.
tournament_test.py -- Test cases for tournament.py

STEPS:
1. Copy all files to your computer
2. Run terminal (Mac\Linux) or command prompt(Windows)
3. Start psql command (for run database shell)
3. In the database shell enter: "CREATE DATABASE tournament;"
4. In the database shell enter: "\c tournament" to connect to database.
5. In the database shell enter commands from tournament.sql file or enter: "\i tournament.sql" to install database schema (tables, views)
6. Exit database shell
7. Run tests by entering "python tournament_test.py" in shell.
8. That's all :)

####################################