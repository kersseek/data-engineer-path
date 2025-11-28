import seaborn as sns
import sqlite3
import pandas as pd
import prettytable

%load_ext sql

con = sqlite3.connect("socioeconomic.db")
cur = con.cursor()

%sql sqlite: // /socioeconomic.db

df = pd.read_csv("https://data.cityofchicago.org/resource/jcxq-k9xf.csv")
df.to_sql("chicago_socioeconomic_data", con,
          if_exists='replace', index=False, method='multi')

prettytable.DEFAULT = 'DEFAULT'

# Verify that the table creation was successful
%sql SELECT * FROM chicago_socioeconomic_data
# How many rows are in the dataset?
%sql SELECT COUNT(*) FROM chicago_socioeconomic_data

# How many community areas in Chicago have a hardship index greater than 50.0?
%sql SELECT COUNT(community_area_name) FROM chicago_socioeconomic_data WHERE hardship_index > 50
# What is the maximum value of hardship index in this dataset?
%sql SELECT MAX(hardship_index) FROM chicago_socioeconomic_data

# Which community area which has the highest hardship index?
%sql SELECT community_area_name FROM chicago_socioeconomic_data WHERE hardship_index IN(SELECT MAX(hardship_index) FROM chicago_socioeconomic_data)
# Which Chicago community areas have per-capita incomes greater than $60,000?
%sql SELECT community_area_name FROM chicago_socioeconomic_data WHERE per_capita_income_ > 60000

# Create a scatter plot using the variables per_capita_income_ and hardship_index. Explain the correlation between the two variables.
income_vs_hardship = %sql SELECT per_capita_income_, hardship_index FROM chicago_socioeconomic_data
plot = sns.jointplot(x='per_capita_income_', y='hardship_index',
                     data=income_vs_hardship.DataFrame())
