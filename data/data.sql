insert into Boroughs values ("Brooklyn");
insert into Boroughs values ("Bronx");
insert into Boroughs values ("Manhattan");
insert into Boroughs values ("Queens");
insert into Boroughs values ("Staten Island");

-- zip_codes_is_in.csv
COPY Zip_Codes_Is_In
FROM 'zip_codes_is_in.csv'
delimiter ','
CSV HEADER;

-- train_stations_have.csv
COPY Zip_Codes_Is_In
FROM 'train_stations_have.csv'
delimiter ','
CSV HEADER;

-- stops_at.csv
COPY Zip_Codes_Is_In
FROM 'stops_at.csv'
delimiter ','
CSV HEADER;

-- train_lines.csv
COPY Zip_Codes_Is_In
FROM 'train_lines.csv'
delimiter ','
CSV HEADER;

-- covid_casualties.csv
COPY Zip_Codes_Is_In
FROM 'covid_casualties.csv'
delimiter ','
CSV HEADER;