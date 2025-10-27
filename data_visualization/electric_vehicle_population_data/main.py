import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

directory_path = os.path.dirname(__file__)
csv_path = os.path.join(directory_path, 'Electric_Vehicle_Population_Data.csv')

def extract_csv(csv_path):
    """ 
    Read a CSV dile and return its content as a DataFrame.
    
    Parameters
    ----------
    csv_path : str
        Path to the CSV file to read.
    
    Returns
    -------
    DataFrame
        DataFrame containing the data from CSV file.
    """
    df = pd.read_csv(csv_path)
    
    # print(df.dtypes)
    # print(df.isna().mean().sort_values(ascending=False))
    # print(df['VIN (1-10)'].value_counts())

    return df

def transform(data_extracted):
    """
    Transform the DataFrame by handling NaN values and renaming columns.
    
    Parameters
    ----------
    data_extracted : DataFrame
        Input DataFrame to transform data.
        
    Returns
    -------
    DataFrame
        DataFrame with NaN values filled (numerical coliumns with media, others with 'unknown')
        and column 'County' renamed to 'Country'.
    """
    data_extracted = data_extracted.rename(columns={'County': 'Country'})
    list_nan = nan_values(data_extracted)
       
    if len(list_nan) != 0:
        for column in list_nan:
            if data_extracted[column].dtypes == 'float64':
                media = data_extracted[column].median()
                data_extracted[column] = data_extracted[column].fillna(media)
            else:
                data_extracted[column] = data_extracted[column].fillna("unknown")
                
        list_nan = nan_values(data_extracted)
        
        if len(list_nan) == 0:
            print("Data handled correctly, It's ready to load and visualize")
        else:
            print(f"There's still inconsistencies: {list_nan}")
    
    return data_extracted

def nan_values(data):
    """
    Count the number of NaN values in each column of a DataFrame.
    
    Parameters
    ----------
    data : DataFrame
        Input DataFrame to analyze.
    
    Returns
    -------
    dict
        Dictionary mapping column names to the number of NaN values.
    """
    list_nan = {}
    
    for column in data.columns:
        count = data[column].isna().value_counts()

        if True in count:
            list_nan[column] = count[True]
        
    return list_nan

def annotated_heatmap(data):
    """ 
    Create an annoted heatmap showing the count of EV by State and Model Year.
    
    Parameters
    ----------
    data : DataFrame
        Input DataFrame containing EV data with columns 'State', 'Model Year' and 'VIN (1-10s)'.
        
    Returns
    -------
    None
        Displays a heatmap plot.
    """
    sns.set_theme()
    
    ev_count_by_state_and_year = data.pivot_table(index='State', columns='Model Year', values="VIN (1-10)", aggfunc='count')
    
    f, ax = plt.subplots(figsize=(35,20))
    sns.heatmap(ev_count_by_state_and_year, annot=True, fmt=".2f", linewidths=.5, ax=ax)
    
def scatterplot_semantics(data):
    """ 
    Create an semantic scatter plot showing the relationship between Model Year and Base MSRP for EV.
    
    Parameters
    ----------
    data : DataFrame
        Input DataFrame containing EV data with columns 'Model Year' and 'Base MSRP'.
        
    Returns
    -------
    None
        Displays a semantic scatter plot.
    """
    sns.set_theme(style="whitegrid")
       
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    sns.despine(f, left=True, bottom=True)

    sns.scatterplot(x="Model Year", y="Base MSRP",
                    palette="ch:r=-.2,d=.3_r",
                    sizes=(1, 8), linewidth=0,
                    data=data, ax=ax)

data = extract_csv(csv_path)
data = transform(data)
annotated_heatmap(data)
scatterplot_semantics(data)
