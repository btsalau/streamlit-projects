import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import re
import base64

warnings.simplefilter(action='ignore', category=FutureWarning)

# Setting The App Title
st.title("F1FA 21 Players Stats Exploratory Analysis")

st.markdown("""18k+ players, 100+ attributes extracted from the 2021 edition of FIFA. Content includes:
* URL of the scraped players
* Player positions, with the role in the club and in the national team
* Player attributes with statistics as Attacking, Skills, Defense, Mentality, GK Skills, etc.
* Player personal data like Nationality, Club, DateOfBirth, Wage, Salary, etc.

Data Source: [FIFA 21 complete player Kaggle dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-21-complete-player-dataset)
""")

# Importing dataframe 
df = pd.read_csv('players_21.csv')

#Create Country Filter from df
country_list = list(np.sort(df.nationality.unique()))

# create sidebar - sidebar can only be to left
st.sidebar.header("Input Features")

# Create Nationality Dropdown Menu
selected_nationality = st.sidebar.selectbox("Select Nationality Filter", country_list)

# function to apply nationality filter to df
def df_filter(nationality):
    nationality = df[df['nationality'] == nationality]
    return nationality

nationality_df = df_filter(selected_nationality)


# function to extract positions from nationality DF
def positions(df):
    player_positions = df.player_positions.str.split(', ')
    dummies = pd.get_dummies(player_positions.apply(pd.Series).stack()).sum(level=0)
    player_positions = list(dummies.columns)
    return player_positions


available_positions = positions(nationality_df)


#  Multi-Select Player Position Filter from Nationality DF
selected_positions = st.sidebar.multiselect(
    label="Available Positions",
    options=available_positions,
    default=available_positions
    )

regex_patterns = '|'.join(selected_positions) # to be used with searching for position


# function to extract positions from nationality DF
available_leagues = list(nationality_df.league_name.unique())

#  Multi-Select League Filter from Nationality DF
selected_leagues = st.sidebar.multiselect(
    label="Select League Filter",
    options=available_leagues,
    default=available_leagues
    )




# Applying League and Position Filter to Nationality DF
filt = (nationality_df['league_name'].isin(selected_leagues)) & (nationality_df['player_positions'].str.contains(regex_patterns))
selected_df = nationality_df.loc[filt, 'short_name']

# Streamlit Main Display
st.header("Displaying Players Available To National Team & Their Stats")

# Write General Info about App
st.write(f"The {selected_nationality} National Team has {selected_df.shape[0]} players available for selection")

st.dataframe(selected_df)

# Download selected df data to csv
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(selected_df), unsafe_allow_html=True)