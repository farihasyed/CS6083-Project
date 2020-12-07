import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser


@st.cache
def get_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f'Running query_db(): {sql}')

    db_info = get_config()

    # Connect to an existing database
    connection = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cursor = connection.cursor()

    # Execute a command: this creates a new table
    cursor.execute(sql)

    # Obtain data
    data = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    # Make the changes to the database persistent
    connection.commit()

    # Close communication with the database
    cursor.close()
    connection.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


def zip_codes_and_neighborhoods(borough):
    return f"""select ZC.zip_code, CCAI.neighborhood 
            from Boroughs B, Zip_Codes_Is_In ZC, COVID_Casualties_Are_In CCAI
            where B.name = '{borough}'
            and B.bid = ZC.bid
            and ZC.zip_code = CCAI.zip_code;
            """


def train_stations(borough):
    return f"""select TSH.zip_code, TSH.name 
            from Train_Stations_Have TSH, Boroughs B, Zip_Codes_Is_In ZC
            where B.name = '{borough}'
            and B.bid = ZC.bid
            and ZC.zip_code = TSH.zip_code;
            """


def train_lines(borough):
    return f"""
            select distinct TL.name, TL.color, TL.speed 
            from Train_Stations_Have TSH, Stops_At SA, Train_Lines TL, Boroughs B, Zip_Codes_Is_In ZC 
            where B.bid = ZC.bid 
            and B.name = '{borough}'
            and ZC.zip_code = TSH.zip_code
            and TSH.name = SA.station_name
            and TL.name = SA.line_name
            """


def accidents(borough):
    return f"""
            select AOI.date, AOI.time, AOI.street_name, AOI.contributing_factor 
            from Accidents_Occurred_In AOI, Boroughs B, Zip_Codes_Is_In ZC 
            where B.bid = ZC.bid 
            and B.name = '{borough}'
            and ZC.zip_code = AOI.zip_code
            """


def covid_casualties(borough):
    return f"""
            select CCAI.zip_code, CCAI.cases, CCAI.deaths
            from COVID_Casualties_Are_In CCAI, Boroughs B, Zip_Codes_Is_In ZC 
            where B.bid = ZC.bid 
            and B.name = '{borough}'
            and ZC.zip_code = CCAI.zip_code
            """


def demographics(borough):
    return f"""
            select ZC.zip_code, ZC.females, ZC.males, ZC.gender_unknown, ZC.American_Indians, ZC.Asians, 
            ZC.Blacks, ZC.Hispanics_Latinos, ZC.Pacific_Islanders, ZC.Whites, ZC.other_ethnicity, 
            ZC.ethnicity_unknown
            from Boroughs B, Zip_Codes_Is_In ZC
            where B.bid = ZC.bid
            and B.name = '{borough}'
            """


def compare_accidents(boroughs):
    start = f"""
            select B.name, count(AOI.collision_id) 
            from Accidents_Occurred_In AOI, Boroughs B, Zip_Codes_Is_In ZC 
            where B.bid = ZC.bid 
            and ZC.zip_code = AOI.zip_code
            and (
        """
    borough_condition = " B.name = "
    end = f"""
            group by B.name
            order by B.name"""

    borough_conditions = []
    for borough in boroughs:
        if borough != boroughs[0]:
            borough_conditions.append(' or ')
        borough_conditions.append(''.join([borough_condition, '\'', borough, '\'']))
    query = ''.join([start, ''.join(borough_conditions), ')', end])
    print(query)
    return query


def compare_covid_casualties(boroughs):
    start = f"""
        select B.name, sum(CCAI.cases) as cases, sum(CCAI.deaths) as deaths 
        from COVID_Casualties_Are_In CCAI, Boroughs B, Zip_Codes_Is_In ZC 
        where B.bid = ZC.bid 
        and ZC.zip_code = CCAI.zip_code
        and (
        """
    borough_condition = " B.name = "
    end = f"""
                group by B.name
                order by B.name"""

    borough_conditions = []
    for borough in boroughs:
        if borough != boroughs[0]:
            borough_conditions.append(' or ')
        borough_conditions.append(''.join([borough_condition, '\'', borough, '\'']))
    query = ''.join([start, ''.join(borough_conditions), ')', end])
    return query


def compare_train_stations_entrances_exits(boroughs):
    start = f"""
            select B.name, sum(MSUI.entries), sum(MSUI.exits), sum(MSUI.full_fare) as full_fare, 
            sum(MSUI.one_day_unlimited) as one_day_unlimited, 
            sum(MSUI.seven_day_unlimited) as seven_day_unlimited, 
            sum(MSUI.fourteen_day_unlimited) as fourteen_day_unlimited, 
            sum(MSUI.thirty_day_unlimited) as thirty_day_unlimited
            from Stations_Entrances_Exits_Are_Part_Of MSUI, Boroughs B, Zip_Codes_Is_In ZC, Train_Stations_Have TSH
            where B.bid = ZC.bid 
            and TSH.name = MSUI.station_name
            and (
        """
    borough_condition = " B.name = "
    end = f"""
            group by B.name
            order by B.name"""

    borough_conditions = []
    for borough in boroughs:
        if borough != boroughs[0]:
            borough_conditions.append(' or ')
        borough_conditions.append(''.join([borough_condition, '\'', borough, '\'']))
    query = ''.join([start, ''.join(borough_conditions), ')', end])
    print(query)
    return query


def compare_demographics(boroughs):
    start = f"""select B.name, sum(ZC.females) as females, sum(ZC.males) as males, 
            sum(ZC.gender_unknown) as gender_unknown, sum(ZC.American_Indians) as American_Indians, 
            sum(ZC.Asians) as Asians, sum(ZC.Blacks) as Blacks, sum(ZC.Hispanics_Latinos) as Hispanics_Latinos, 
            sum(ZC.Pacific_Islanders) as Pacific_Islanders, sum(ZC.Whites) as Whites,
            sum(ZC.other_ethnicity) as other_ethnicity, sum(ZC.ethnicity_unknown) as ethnicity_unknown
            from Boroughs B, Zip_Codes_Is_In ZC
            where B.bid = ZC.bid
            and (
        """
    borough_condition = " B.name = "
    end = f"""
            group by B.name
            order by B.name"""

    borough_conditions = []
    for borough in boroughs:
        if borough != boroughs[0]:
            borough_conditions.append(' or ')
        borough_conditions.append(''.join([borough_condition, '\'', borough, '\'']))
    query = ''.join([start, ''.join(borough_conditions), ')', end])
    print(query)
    return query


def query_topic(topic, borough_, compare=False):
    if topic == 'Train Stations':
        sql_query = train_stations(borough_)
    elif topic == 'Zip Codes':
        sql_query = zip_codes_and_neighborhoods(borough_);
    elif topic == 'Train Lines':
        sql_query = train_lines(borough_)
    elif topic == 'Accidents':
        sql_query = compare_accidents(borough_) if compare else accidents(borough_)
    elif topic == 'COVID Casualties':
        sql_query = compare_covid_casualties(borough_) if compare else covid_casualties(borough_)
    elif topic == 'Demographics':
        sql_query = compare_demographics(borough_) if compare else demographics(borough_)
    elif topic == 'Train Station Entrances and Exits':
        sql_query = compare_train_stations_entrances_exits(borough_)
    if sql_query:
        return query_db(sql_query)


'## Read tables'

sql_all_table_names = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
all_table_names = query_db(sql_all_table_names)['relname'].tolist()
table_name = st.selectbox('Choose a table', all_table_names)
if table_name:
    f'Display the table'
    sql_table = f'select * from {table_name};'
    df = query_db(sql_table)
    st.dataframe(df)


'## Query Borough'

sql_boroughs = 'select * from boroughs;'
boroughs_table = query_db(sql_boroughs)
boroughs = boroughs_table['name'].tolist()
borough = st.selectbox('Choose a borough', boroughs)
queries = ['Zip Codes', 'Train Stations', 'Train Lines', 'COVID Casualties', 'Accidents', 'Demographics']
query = st.selectbox('Choose a topic to query', queries)
if borough and query:
    query_results = st.dataframe(query_topic(query, borough))


'## Compare Boroughs'

borough_selection = st.multiselect('Choose a borough', boroughs)
queries = ['COVID Casualties', 'Demographics', 'Train Station Entrances and Exits', 'Accidents']
query = st.selectbox('Choose a topic to query', queries)
if len(borough_selection) > 0 and query:
    st.dataframe(query_topic(query, borough_selection, True))



