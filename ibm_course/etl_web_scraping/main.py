import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
csv_path = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv'

table_attribs = ['Name', 'Market cap']

database_name = 'Banks.db'
table_name = 'Largest_banks'

output_path = './Largest_banks_data.csv'
log_file = 'code_log.txt'

sql_connection = sqlite3.connect(database_name)


def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, 'a') as f:
        f.write(timestamp + ' : ' + message + '\n')


def extract(url, table_attribs):
    data_extracted = requests.get(url).text
    soup = BeautifulSoup(data_extracted, 'html.parser')

    df = pd.DataFrame(columns=table_attribs)

    tables = soup.find_all("tbody")
    rows = tables[0].find_all("tr")

    for row in rows:
        col = row.find_all("td")
        if len(col) != 0:
            if col[1].find_all("a") is not None:
                dict_list = {'Name': col[1].find_all("a")[1].contents[0],
                             'Market cap': float(col[2].contents[0].replace('\n', ''))}
                df1 = pd.DataFrame(dict_list, index=[0])
                df = pd.concat([df, df1], ignore_index=True)
    return df


def transform(df, csv_path):
    df_csv = pd.read_csv(csv_path)
    list_dict = df_csv.set_index('Currency').to_dict()['Rate']

    df['MC_GBP_Billion'] = [np.round(x*list_dict['GBP'], 2)
                            for x in df['Market cap']]
    df['MC_EUR_Billion'] = [np.round(x*list_dict['EUR'], 2)
                            for x in df['Market cap']]
    df['MC_INR_Billion'] = [np.round(x*list_dict['INR'], 2)
                            for x in df['Market cap']]

    return df


def load_to_csv(df, output_path):
    df.to_csv(output_path)


def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


def run_query(query_statement, sql_connection):
    return pd.read_sql(query_statement, sql_connection)


log_progress('Starting extraction process')
df = extract(url, table_attribs)
log_progress('Extraction process completed')

log_progress('Starting transformation process')
df = transform(df, csv_path)
log_progress('Transformation process completed')

log_progress('Starting CSV load process')
load_to_csv(df, output_path)
log_progress('CSV load process completed')

log_progress('Starting database load process')
load_to_db(df, sql_connection, table_name)
log_progress('Database load process completed')

log_progress('Starting query execution')
print(run_query('SELECT * FROM Largest_banks', sql_connection))
print(run_query('SELECT AVG(MC_GBP_Billion) FROM Largest_banks', sql_connection))
print(run_query('SELECT Name from Largest_banks LIMIT 5', sql_connection))
log_progress('Query execution completed')
