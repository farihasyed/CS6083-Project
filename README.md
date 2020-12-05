# CS6083 Final Project

## [project.py](code/project.py)
~~I think where the streamlit code will go. Right now, just has a couple of functions from demo.py.~~
Put in streamlit code but haven't tested it yet.

## [data.py](data/data.py)
Python code to scrape data for insertion into database. 

Status of data scraped by table:

* ~~Boroughs~~ [complete](data/data.sql)
* ~~Zip_Codes_Is_In~~ [complete](data/zip_codes_is_in.csv)
* ~~COVID_Casualties_Are_In~~ [complete](data/covid_casualties.csv)
* Accidents_Occurred_In - Cicy
* ~~Train_Stations_Have~~ [complete](data/train_stations_have.csv)
* Turnstiles_Access - Cicy
* ~~Stops_At~~ [complete](data/stops_at.csv)
* ~~Train_Lines~~ [complete](data/train_lines.csv)
* Metrocard_Swipes_Used_At - Cicy

## [schema.sql](code/schema.sql)
Database schema - had to update some things like COVID table. Need to remember to update ER diagram to reflect
these changes.

~~## [data.sql](data/data.sql)~~

~~SQL file to insert CSV files generated from data.py into database. Thought it'd best if 
separate from schema.sql just because schema.sql is so long~~

Easier to read in CSV files into tables via CLI commands, so replaced this with [create_database.sh](create_database.sh)

## [create_database.sh](create_database.sh)
Script to initialize database. Runs [schema.sql](code/schema.sql) and reads in CSV files


    