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


'## Read tables'

sql_all_table_names = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
all_table_names = query_db(sql_all_table_names)['relname'].tolist()
table_name = st.selectbox('Choose a table', all_table_names)
if table_name:
    f'Display the table'

    sql_table = f'select * from {table_name};'
    df = query_db(sql_table)
    st.dataframe(df)

# NOTE
#  queries
#  train stations in each zip code and borough?
#  train stations in each borough
#  covid casualties in each borough
#  accidents in each borough
#  metrocard swipes in each borough
#  demographics per borough
#  lines at each station


def zip_codes_and_neighborhoods():
    return f"""select ZC.zip_code, CCAI.neighborhood 
            from Boroughs B, Zip_Codes_Is_In ZC, COVID_Casualties_Are_In CCAI
            where B.name = '{borough}'
            and B.bid = ZC.bid
            and ZC.zip_code = CCAI.zip_code;
            """


def train_stations():
    return f"""select TSH.name 
            from Train_Stations_Have TSH, Boroughs B, Zip_Codes_Is_In ZC
            where B.name = '{borough}'
            and B.bid = ZC.bid
            and ZC.zip_code = TSH.zip_code;
            """


def train_lines():
    return f"""
            select distinct TL.name, TL.color, TL.speed 
            from Train_Stations_Have TSH, Stops_At SA, Train_Lines TL, Boroughs B, Zip_Codes_Is_In ZC 
            where B.bid = ZC.bid 
            and B.name = '{borough}'
            and ZC.zip_code = TSH.zip_code
            and TSH.name = SA.station_name
            and TL.name = SA.line_name
            """


def accidents():
    return f"""
            select AOI.date, AOI.time, AOI.street_name, AOI.contributing_factor 
            from Accidents_Occurred_In AOI, Boroughs B, Zip_Codes_Is_In ZC 
            where B.bid = ZC.bid 
            and B.name = '{borough}'
            and ZC.zip_code = AOI.zip_code
            """


def covid_casualties():
    return f"""
            select sum(CCAI.cases) as cases, sum(CCAI.deaths) as deaths 
            from COVID_Casualties_Are_In CCAI, Boroughs B, Zip_Codes_Is_In ZC 
            where B.bid = ZC.bid 
            and B.name = '{borough}'
            and ZC.zip_code = CCAT.zip_code
            """


def demographics():
    return f"""
            select sum(ZC.females) as females, sum(ZC.males) as males, sum(ZC.gender_unknown) as gender_unknown,
            sum(ZC.American_Indians) as American_Indians, sum(ZC.Asians) as Asians, sum(ZC.Blacks) as Blacks,
            sum(ZC.Hispanics_Latinos) as Hispanics_Latinos, sum(ZC.Pacific_Islanders) as Pacific_Islanders, 
            sum(ZC.Whites) as Whites, sum(ZC.other_ethnicity) as other_ethnicity, 
            sum(ZC.ethnicity_unknown) as ethnicity_unknown
            from Boroughs B, Zip_Codes_Is_In ZC
            where B.bid = ZC.bid
            and B.name = '{borough}'
            """


def metrocard_swipes():
    return f"""
            select ZC.zip_code, sum(MSUI.full_fare) as full_fare, sum(MSUI.one_day_unlimited) as one_day_unlimited, 
            sum(MSUI.seven_day_unlimited) as seven_day_unlimited, 
            sum(MSUI.fourteen_day_unlimited) as fourteen_day_unlimited, 
            sum(MSUI.thirty_day_unlimited) as thirty_day_unlimited
            from Metrocard_Swipes_Used_At MSUI, Boroughs B, Zip_Codes_Is_In ZC, Train_Stations_Have 
            where B.bid = ZC.bid 
            and B.name = '{borough}'
            group by ZC.zip_code
            and TSH.name = MSUI.station_name
            """


def compare_covid_casualties():
    return f"""
            select B.name, sum(CCAI.cases) as cases, sum(CCAI.deaths) as deaths 
            from COVID_Casualties_Are_In CCAI, Boroughs B, Zip_Codes_Is_In ZC 
            where B.bid = ZC.bid 
            and ZC.zip_code = CCAT.zip_code
            group by B.name
            """


def compare_metrocard_swipes():
    return f"""
            select B.name, sum(MSUI.full_fare) as full_fare, sum(MSUI.one_day_unlimited) as one_day_unlimited, 
            sum(MSUI.seven_day_unlimited) as seven_day_unlimited, 
            sum(MSUI.fourteen_day_unlimited) as fourteen_day_unlimited, 
            sum(MSUI.thirty_day_unlimited) as thirty_day_unlimited
            from Metrocard_Swipes_Used_At MSUI, Boroughs B, Zip_Codes_Is_In ZC, Train_Stations_Have 
            where B.bid = ZC.bid 
            and TSH.name = MSUI.station_name
            group by B.name
            """


def compare_demographics():
    return """select sum(ZC.females) as females, sum(ZC.males) as males, sum(ZC.gender_unknown) as gender_unknown,
        sum(ZC.American_Indians) as American_Indians, sum(ZC.Asians) as Asians, sum(ZC.Blacks) as Blacks,
        sum(ZC.Hispanics_Latinos) as Hispanics_Latinos, sum(ZC.Pacific_Islanders) as Pacific_Islanders, sum(ZC.Whites) as Whites,
        sum(ZC.other_ethnicity) as other_ethnicity, sum(ZC.ethnicity_unknown) as ethnicity_unknown
        from Boroughs B, Zip_Codes_Is_In ZC
        where B.bid = ZC.bid
        """

def query_topic(topic, compare = False):
    if query == 'Train Stations':
        sql_query = train_stations()
    elif query == 'Zip Codes':
        sql_query = zip_codes_and_neighborhoods();
    elif query == 'Train Lines':
        sql_query = train_lines()
    elif query == 'Accidents':
        sql_query = accidents()
    elif query == 'COVID Casualties':
        sql_query = compare_covid_casualties() if compare else covid_casualties()
    elif query == 'Demographics':
        sql_query = compare_demographics() if compare else demographics()
    elif query == 'Metrocard Swipes':
        sql_query = compare_metrocard_swipes() if compare else metrocard_swipes()
    if sql_query:
        return query_db(sql_query).loc[0]


'## Query Borough'

queries = ['Zip Codes', 'Train Stations', 'Train Lines', 'COVID Casualties', 'Accidents', 'Demographics',
           'Metrocard Swipes']
query = st.selectbox('Choose a topic to query', queries)
if query:
    sql_boroughs = 'select * from boroughs;'
    boroughs_table = query_db(sql_boroughs).loc[0]
    boroughs = boroughs_table['name'].tolist()
    borough = st.selectbox('Choose a borough', boroughs)
    if borough:
        query_results = query_topic(query)

'## Compare Boroughs'

queries = ['COVID Casualties', 'Demographics', 'Metrocard Swipes']
query = st.selectbox('Choose a topic to query', queries)
if query:
    query_results = query_topic(query)