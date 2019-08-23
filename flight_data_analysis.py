#%% [markdown]
# # 2015 Flight Delays and Cancellations
#
#![Airport departures](https://images.unsplash.com/photo-1421789497144-f50500b5fcf0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60 "Flights")
#
# Photo by Matthew Smith on Unsplash.
#
# ### Which airline should you fly on to avoid significant delays?
#
#
# The U.S. Department of Transportation's (DOT) Bureau of Transportation 
# Statistics tracks the on-time performance of domestic flights operated 
# by large air carriers. Summary information on the number of on-time, delayed, 
# canceled, and diverted flights is published in DOT's monthly Air Travel Consumer 
# Report and in this dataset of 2015 flight delays and cancellations.
#
# The flight delay and cancellation data was collected and published by the DOT's Bureau of Transportation Statistics.

#%% [markdown]
# ## Datasets
# ### We will work with 3 dataset collected by the DOT's Bureau of Transportation Statistics.
'''
- airlines
- airports
- flights
'''

#%% [markdown]
# ## Library Imports
#%%
import pandas as pd 
import numpy as np 
import plotly
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import matplotlib.pyplot as plt 
import seaborn as sns 
from datetime import datetime

sns.set(style="whitegrid")
# warnings.filterwarnings("ignore")

#%% [markdown]
# ## Load Datasets
#%%
def load_datasets():
    airlines = pd.read_csv('data/airlines.csv')
    airports = pd.read_csv('data/airports.csv')
    flights = pd.read_csv('data/flights.csv')
    return (airlines, airports, flights)

datasets = load_datasets()

#%%
airlines_df = datasets[0]
airports_df = datasets[1]
flights_df = datasets[2]

#%% [markdown]
# Lets take a look at the first few lines of each dataset
#


#%% [markdown]
# #### Airlines
#%%
airlines_df.head()
#%%
print(f'Dataframe has {airlines_df.shape[0]} rows, and {airlines_df.shape[1]} columns.')


#%% [markdown]
# #### Airports
#%%
airports_df.head()
#%%
print(f'Dataframe has {airports_df.shape[0]} rows, and {airports_df.shape[1]} columns.')


#%% [markdown]
# #### Flights
#%%
weekday_dict = {
    1 : 'Monday',
    2 : 'Tuesday',
    3 : 'Wednesday',
    4 : 'Thursday',
    5 : 'Friday',
    6 : 'Saturday',
    7 : 'Sunday',
}

flights_df['DAY_OF_WEEK'] = flights_df['DAY_OF_WEEK'].map(weekday_dict)
flights_df['flight_date'] = [datetime(year, month, day) for year, month, day in zip(flights_df.YEAR, flights_df.MONTH, flights_df.DAY)]
flights_df.head()
#%%
print(f'Dataframe has {flights_df.shape[0]} rows, and {flights_df.shape[1]} columns.')


#%% [markdown]
# ### Lets combine these dataframes in to one.
#
#%%
# Rename airline code column.
airlines_df.rename(columns={'IATA_CODE':'AIRLINE_CODE'}, inplace=True)
# Rename airport code column.
airports_df.rename(columns={'IATA_CODE':'AIRPORT_CODE'}, inplace=True)
# Rename flights airline code column.
flights_df.rename(columns={'AIRLINE':'AIRLINE_CODE'}, inplace=True)
# Rename flights origin code column.
flights_df.rename(columns={'ORIGIN_AIRPORT':'ORIGIN_AIRPORT_CODE'}, inplace=True)
# Rename flights destination code column.
flights_df.rename(columns={'DESTINATION_AIRPORT':'DESTINATION_AIRPORT_CODE'}, inplace=True)



#%% [markdown]
# #### We merge flights_df and airlines_df on 'AIRLINE' column.
#%%
combined_df = pd.merge(flights_df, airlines_df, on='AIRLINE_CODE', how='left')

#%% [markdown]
# #### We merge flights_df and airports_df on 'ORIGIN_AIRPORT_CODE' column.
#%%
combined_df = pd.merge(combined_df, airports_df, left_on='ORIGIN_AIRPORT_CODE', right_on='AIRPORT_CODE', how='left')

#%% [markdown]
# #### We merge flights_df and airports_df on 'DESTINATION_AIRPORT_CODE' column.
#%%
combined_df = pd.merge(combined_df, airports_df, left_on='DESTINATION_AIRPORT_CODE', right_on='AIRPORT_CODE', how='left')

# Caculating flight airtime
combined_df['elapsed_time'] = combined_df['WHEELS_ON'] - combined_df['WHEELS_OFF']

#%% [markdown]
# #### There are null values throughout the CANCELLATION_REASON, AIR_SYSTEM_DELAY, SECURITY_DELAY, AIRLINE_DELAY, LATE_AIRCRAFT_DELAY, and WEATHER_DELAY columns.
# #### I decide to fill the null values with 0.0.
#%%
combined_df.fillna(value=0.0, inplace=True)

#%%
combined_df.head()

#%%
# Rename origin airport meta columns.
combined_df.rename(columns={'AIRPORT_x':'ORIGIN_AIRPORT', 
                            'CITY_x':'ORIGIN_CITY', 
                            'STATE_x':'ORIGIN_STATE',
                            'COUNTRY_x':'ORIGIN_COUNTRY',
                            'LATITUDE_x':'ORIGIN_LATITUDE',
                            'LONGITUDE_x':'ORIGIN_LONGITUDE'}, inplace=True)

#%%
# Rename destination airport meta columns.
combined_df.rename(columns={'AIRPORT_y':'DESTINATION_AIRPORT', 
                            'CITY_y':'DESTINATION_CITY', 
                            'STATE_y':'DESTINATION_STATE',
                            'COUNTRY_y':'DESTINATION_COUNTRY',
                            'LATITUDE_y':'DESTINATION_LATITUDE',
                            'LONGITUDE_y':'DESTINATION_LONGITUDE'}, inplace=True)

#%% [markdown]
# ## Origin Airport Distribution
#%%
number_of_flights = combined_df.shape[0]
#%%
origin_airport_group = combined_df.groupby('ORIGIN_AIRPORT')['FLIGHT_NUMBER'].count().sort_values(ascending=False)


#%% [markdown]
# ## Airline Distribution
#%%
airline_group = combined_df.groupby('AIRLINE')['FLIGHT_NUMBER'].count().sort_values(ascending=False)


#%%
origin_airport_group[1:11]

#%%
airline_group[:10]



#%%
