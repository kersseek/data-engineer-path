import pandas as pd
import sqlite3
import prettytable

url_chicago_census_data = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCensusData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01'
url_chicago_public_schools = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoPublicSchools.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01'
url_chicago_crime_data = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCrimeData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01'

db_name = 'FinalDB.db'

df_chicago_census_data = pd.read_csv(url_chicago_census_data)
df_chicago_public_schools = pd.read_csv(url_chicago_public_schools)
df_chicago_crime_data = pd.read_csv(url_chicago_crime_data)

%load_ext sql

con = sqlite3.connect(db_name)
cur = con.cursor()

%sql sqlite: // /FinalDB.db

df_chicago_census_data.to_sql(
    'CENSUS_DATA', con, if_exists='replace', index=False, method='multi')
df_chicago_public_schools.to_sql(
    'CHICAGO_PUBLIC_SCHOOLS', con, if_exists='replace', index=False, method='multi')
df_chicago_crime_data.to_sql(
    'CHICAGO_CRIME_DATA', con, if_exists='replace', index=False, method='multi')

prettytable.DEFAULT = 'DEFAULT'

# Find the total number of crimes recorded in the CRIME table
%sql SELECT COUNT(*) FROM CHICAGO_CRIME_DATA
# List all case numbers for crimes involving minors?(children are not considered minors for the purposes of crime analysis)
%sql SELECT ID, CASE_NUMBER, DESCRIPTION FROM CHICAGO_CRIME_DATA WHERE DESCRIPTION LIKE '%minor%' AND DESCRIPTION NOT LIKE '%child%'
# List all kidnapping crimes involving a child?
%sql SELECT ID, CASE_NUMBER, DESCRIPTION FROM CHICAGO_CRIME_DATA WHERE DESCRIPTION LIKE '%child%'
# List the kind of crimes that were recorded at schools. (No repetitions)
%sql SELECT DISTINCT ID, CASE_NUMBER, DESCRIPTION, LOCATION_DESCRIPTION FROM CHICAGO_CRIME_DATA WHERE LOCATION_DESCRIPTION LIKE '%school%'

# List the type of schools along with the average safety score for each type
%sql SELECT[ELEMENTARY, MIDDLE, OR HIGH SCHOOL], AVG(SAFETY_SCORE) FROM CHICAGO_PUBLIC_SCHOOLS GROUP BY[ELEMENTARY, MIDDLE, OR HIGH SCHOOL]

# List community area names and numbers with per capita income less than 11000
%sql SELECT COMMUNITY_AREA_NAME FROM CENSUS_DATA WHERE PER_CAPITA_INCOME < 11000
# List 5 community areas with highest % of households below poverty line
%sql SELECT COMMUNITY_AREA_NAME, PERCENT_HOUSEHOLDS_BELOW_POVERTY FROM CENSUS_DATA ORDER BY PERCENT_HOUSEHOLDS_BELOW_POVERTY DESC LIMIT 5
# Use a sub-query to find the name of the community area with highest hardship index
%sql SELECT COMMUNITY_AREA_NAME, HARDSHIP_INDEX FROM CENSUS_DATA WHERE HARDSHIP_INDEX = (SELECT MAX(HARDSHIP_INDEX) FROM CENSUS_DATA)
# Use a sub-query to determine the Community Area Name with most number of crimes?
%sql SELECT COMMUNITY_AREA_NAME FROM CENSUS_DATA WHERE COMMUNITY_AREA_NUMBER = (SELECT COMMUNITY_AREA_NUMBER FROM CHICAGO_CRIME_DATA GROUP BY COMMUNITY_AREA_NUMBER ORDER BY COUNT(*) DESC LIMIT 1)
