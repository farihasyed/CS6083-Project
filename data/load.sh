psql -U fs1688 -d fs1688_project -a -f data/load.sql
cat data/zip_codes_is_in.csv | psql -U fs1688 -d fs1688_project -h localhost -p 5432 -c "copy Zip_Codes_Is_In from stdin csv header"
cat data/covid_casualties.csv | psql -U fs1688 -d fs1688_project -h localhost -p 5432 -c "copy COVID_Casualties_Are_In from stdin csv header"
cat data/train_lines.csv | psql -U fs1688 -d fs1688_project -h localhost -p 5432 -c "copy Train_Lines from stdin csv header"
cat data/train_stations_have.csv | psql -U fs1688 -d fs1688_project -h localhost -p 5432 -c "copy Train_Stations_Have from stdin csv header"
cat data/stops_at.csv | psql -U fs1688 -d fs1688_project -h localhost -p 5432 -c "copy Stops_At from stdin csv header"
cat data/accidents_occurred_in.csv | psql -U fs1688 -d fs1688_project -h localhost -p 5432 -c "copy accidents_occured_in from stdin csv header"
cat data/metrocard_swipes_used_at.csv | psql -U fs1688 -d fs1688_project -h localhost -p 5432 -c "copy metrocard_swipes_used_at from stdin csv header"
cat data/turnstiles_access.csv | psql -U fs1688 -d fs1688_project -h localhost -p 5432 -c "copy turnstiles_access from stdin csv header"

