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
airports_df.rename(columns={'IATA_CODE':'ORIGIN_AIRPORT'}, inplace=True)
# Rename flights airline code column.
flights_df.rename(columns={'AIRLINE':'AIRLINE_CODE'}, inplace=True)

#%% [markdown]
# We merge flights_df and airlines_df on 'AIRLINE' column.
#%%
combined_df = pd.merge(flights_df, airlines_df, on='AIRLINE_CODE', how='left')

#%% [markdown]
# We merge flights_df and airports_df on 'ORIGIN_AIRPORT' column.
#%%
combined_df = pd.merge(combined_df, airports_df, on='ORIGIN_AIRPORT', how='left')

#%%
combined_df.fillna(value=0.0, inplace=True)