# CS6083 Final Project

## [project.py](src/project.py)
I think where the streamlit code will go. Right now, just has a couple of functions from demo.py.

## [data.py](src/data.py)
Python code to scrape data for insertion into database. 

Status of data scraped by table:

* ~~Boroughs~~ [complete](data/data.sql)
* ~~Zip_Codes_Is_In~~ [complete](data/zip_codes_is_in.csv)
* COVID_Casualties_Are_In
* Accidents_Occurred_In
* ~~Train_Stations_Have~~ [complete](data/train_stations_have.csv)
* Turnstiles_Access
* ~~Stops_At~~ [complete](data/stops_at.csv)
* ~~Train_Lines~~ [complete](data/train_lines.csv)
* Metrocard_Swipes_Used_At

## [schema.sql](data/schema.sql)
Database schema

## [data.sql](data/data.sql)
SQL file to insert CSV files generated from data.py into database. Thought it'd best if 
separate from schema.sql just because schema.sql is so long


    