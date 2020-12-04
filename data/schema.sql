-- TODO modify ER diagram based on changes
drop table if exists Boroughs cascade;
drop table if exists Zip_Codes_Boroughs cascade;
drop table if exists Demographics cascade;
drop table if exists Zip_Codes_Is_In cascade;
drop table if exists COVID_Casualties_Are_In cascade;
drop table if exists Accidents_Occurred_In cascade;
drop table if exists Train_Stations_Have cascade;
drop table if exists Turnstiles_Access cascade;
drop table if exists Stops_At cascade;
drop table if exists Train_Lines cascade;
drop table if exists Metrocard_Swipes_Used_At cascade;

create table Boroughs (
    bid serial primary key,
    name varchar(32) unique not null
);

insert into Boroughs (name) values ('Brooklyn');
insert into Boroughs (name) values ('Bronx');
insert into Boroughs (name) values ('Manhattan');
insert into Boroughs (name) values ('Queens');
insert into Boroughs (name) values ('Staten Island');

create table Zip_Codes_Is_In (
    zip_code integer primary key,
    bid integer not null,
    females integer,
    males integer,
    gender_unknown integer,
    American_Indians integer,
    Asians integer,
    Blacks integer,
    Hispanics_Latinos integer,
    Pacific_Islanders integer,
    Whites integer,
    other_ethnicity integer,
    ethnicity_unknown integer,
    foreign key (bid) references Boroughs(bid)
);

-- had to modify because data that's by zip code is cumulative and lacks dates
-- how would this change in ER diagram?
create table COVID_Casualties_Are_In (
    zip_code integer primary key,
    neighborhood varchar(256),
    cases integer not null,
    deaths integer not null,
    foreign key (zip_code) references Zip_Codes_Is_In (zip_code)
);

create table Accidents_Occurred_In (
    collision_id integer primary key,
    zip_code integer not null,
    date date,
    time time,
    street_name varchar(32),
    contributing_factor varchar(32),
    foreign key (zip_code) references Zip_Codes_Is_In(zip_code)
);

create table Train_Stations_Have (
    name varchar(64) primary key,
    zip_code integer not null,
    foreign key (zip_code) references Zip_Codes_Is_In(zip_code)
);

-- alter table Train_Stations_Have add foreign key (zip_code) references Zip_Codes_Is_In(zip_code);

create table Turnstiles_Access (
    turnstile_id integer,
    station_name varchar(64),
    date date,
    time timestamp,
    entries integer,
    exits integer,
    primary key (station_name, turnstile_id, date, time),
    foreign key (station_name) references Train_Stations_Have(name) on delete cascade
);

create table Train_Lines (
    name varchar(4) primary key,
    color varchar(16),
    speed varchar(8)
);

create table Stops_At (
    station_name varchar(64),
    line_name varchar(4),
    primary key (station_name, line_name),
    foreign key (station_name) references Train_Stations_Have(name),
    foreign key (line_name) references Train_Lines(name)
);

create table Metrocard_Swipes_Used_At (
    from_date date,
    to_date date,
    full_fare integer,
    one_day_unlimited integer,
    seven_day_unlimited integer,
    fourteen_day_unlimited integer,
    thirty_day_unlimited integer,
    station_name varchar(64),
    primary key (from_date, to_date, station_name),
    foreign key (station_name) references Train_Stations_Have(name)
);