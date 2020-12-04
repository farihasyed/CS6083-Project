psql -U fs1688 -d fs1688 -a -f schema.sql

cat zip_codes_is_in.csv | psql -U fs1688 -d fs1688-db -h localhost -p 5432 -c "copy Zip_Codes_Is_In from stdin csv header"
cat covid_casualties.csv | psql -U fs1688 -d fs1688-db -h localhost -p 5432 -c "copy COVID_Casualties_Are_In from stdin csv header"
cat train_lines.csv | psql -U fs1688 -d fs1688-db -h localhost -p 5432 -c "copy Train_Lines from stdin csv header"
cat train_stations_have.csv | psql -U fs1688 -d fs1688-db -h localhost -p 5432 -c "copy Train_Stations_Have from stdin csv header"
cat stops_at.csv | psql -U fs1688 -d fs1688-db -h localhost -p 5432 -c "copy Stops_At from stdin csv header"

