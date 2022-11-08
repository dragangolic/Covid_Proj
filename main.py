import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime


covid_df = pd.read_csv("C:/Users/golic/OneDrive/Desktop/Covid-India/covid_19_india.csv")
# print(covid_df.head(50))
# display(covid_df.head())
vaccine_df = pd.read_csv("C:/Users/golic/OneDrive/Desktop/Covid-India/covid_vaccine_statewise.csv")
# print(vaccine_df.head(7))
covid_df.drop(["Sno", "Time", "ConfirmedIndianNational", "ConfirmedForeignNational"], inplace=True, axis=1)
# print(covid_df.head(10))
covid_df['Date'] = pd.to_datetime(covid_df['Date'], format='%Y-%m-%d')
# print(covid_df.head(10))

# total number of active cases(number of confirmed - (cured + deaths reported)
covid_df['Active_Cases'] = covid_df['Confirmed'] - (covid_df['Cured'] + covid_df['Deaths'])
# print(covid_df.tail())

# clear the pivot table - sum of the...
statewise = pd.pivot_table(covid_df, values=['Confirmed', 'Deaths', 'Cured'], index="State/UnionTerritory", aggfunc=max)

# Recovery rate (total number of Cured Cases / total number of confirmed cases in 200)
statewise["Recovery Rate"] = statewise["Cured"]*100/statewise["Confirmed"]
# print(statewise.head())

# Mortality rate
statewise["Mortality Rate"] = statewise["Deaths"]*100/statewise["Confirmed"]
# print(statewise.head())
# print(covid_df.tail())

# Sort the values based on Confirmed cases col in desc order
statewise = statewise.sort_values(by='Confirmed', ascending=False)
# print(statewise.head())

# Plot the pivot table(using visual. background_gradiant function will pass out cmap parameter
statewise.style.background_gradient(cmap="cubehelix")
print(statewise.head(15))

# top 10 active cases states
top_10_active_cases = covid_df.groupby(by='State/UnionTerritory').max()[['Active_Cases', 'Date']]. sort_values(by=['Active_Cases'], ascending=False).reset_index()
fig = plt.figure(figsize=(16, 9))
plt.title("Top 10 states with most active cases in India", size=25)
plt.show()

# Top 10 states with highest deaths
top_10_deaths = covid_df.groupby(by='State/UnionTerritory').max()[['Deaths', 'Date']].sort_values(by=['Deaths'], ascending=False).reset_index()
fig = plt.figure(figsize=(18, 5))
plt.title("Top 10 states with most Deaths", size=25)
ax = sns.barplot(data=top_10_deaths.iloc[:12], y="Deaths", x="State/UnionTerritory", linewidth=2, edgecolor='purple')
plt.xlabel("States")
plt.ylabel("Total Death Cases")
# plt.show()


# Growth trend
fig = plt.figure(figsize=(12, 6))
ax = sns.lineplot(data=covid_df[covid_df['State/UnionTerritory'].isin(['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Uttar Pradesh'], x='Date', y='Active_Cases', hue='State/UnionTerritory')])
ax.set_title("Top 5 Affected States in India", size=16)

# Changine column name
vaccine_df.rename(columns = {'Updated On' : 'Vaccine_Date'}, inplace= True)
vaccine_df.head()
vaccine_df.info()

# Find missing values for each column
vaccine_df.isnull().sum(0)

# Drop few missing value columns
vaccination = vaccine_df.drop(columns = ['Sputnik V (Doses Administered)', 'AEFI', '18-44 Years (Doses Administered)','45-60 Years (Doses Administered)', '60+ Years (Doses Administered)'], axis=1)
vaccination.head()


# Male vs Female vaccination
male = vaccination["Male(Individuals Vaccinated)"].sum()
female = vaccination["Female(Individuals Vaccinated)"].sum()
px.pie(names=["Male", "Female"], values = [male, female], title = "Male and Female Vaccination")