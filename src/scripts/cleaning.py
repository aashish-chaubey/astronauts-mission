
import numpy as np
import pandas as pd

mission = "../../data/missions.csv"
mission_df = pd.read_csv(mission, index_col='ID').drop(columns=['Unnamed: 0'])

astronauts = "../../data/astronauts.csv"
astronauts_df = pd.read_csv(astronauts).drop(columns=['Unnamed: 0', 'id', 'original_name'])
astronauts_df = astronauts_df.rename(columns={"field21": "eva"})

###
#   Cleaning astronauts dataset
###

astronauts_df['occupation'] = astronauts_df['occupation'].str.lower()
astronauts_df['occupation'] = np.where((astronauts_df['occupation'] == 'space tourist'),
                                      'other (space tourist)',
                                       astronauts_df['occupation'])

astronauts_df = astronauts_df.drop(['mission_number', 'total_number_of_missions', 'total_hrs_sum', 'total_eva_hrs', 'nationwide_number'], axis=1)

# # Fixing missing values for the shuttle names
missing_shuttles = astronauts_df.loc[astronauts_df['ascend_shuttle'].isna()].copy()
missing_shuttles.loc[:, ['ascend_shuttle', 'descend_shuttle']] = missing_shuttles['in_orbit'].item()
astronauts_df.loc[astronauts_df['ascend_shuttle'].isna()] = missing_shuttles

# Fixing missing values for mission title column
missing_mission_titles = astronauts_df.loc[astronauts_df['mission_title'].isna()].copy()
missing_mission_titles.loc[:, 'mission_title'] = 60
astronauts_df.loc[astronauts_df['mission_title'].isna()] = missing_mission_titles

# Fixing missing values for select column
missing_selection = astronauts_df.loc[astronauts_df['selection'].isna()].copy()
missing_selection.loc[:, 'selection'] = 'MirCorp'
astronauts_df.loc[astronauts_df['selection'].isna()] = missing_selection

###
#   Cleaning mission dataset
###

mission_df['Cost'] = mission_df['Cost'].str.replace(',', '')
mission_df['Cost'] = pd.to_numeric(mission_df['Cost'])

mission_df.loc[mission_df['Company Name'] == "Arm??e de l'Air", ['Company Name']] = "Arme de l'Air"

# Extract country for faster processing of the data
mission_df['Country'] = mission_df['Location'].str.extract(r'^.*?([^\t,]*)$')
mission_df['Country'] = mission_df['Country'].str.strip()

# Normalizing the Details for faster processing
mission_df[['Vehicle', 'Mission']] = mission_df['Detail'].str.split('|', expand=True)
mission_df['Mission'] = mission_df['Mission'].str.strip(' ')
mission_df['Vehicle'] = mission_df['Vehicle'].str.strip(' ')

mission_df['Status Rocket'] = mission_df['Status Rocket'].replace({'StatusActive':'Active', 'StatusRetired':'Retired'})

mission_df = mission_df.drop('Detail', axis=1)

# Write the data back to the excel file for next steps
with pd.ExcelWriter('../../data/cleaned_data.xlsx') as writer:  
    astronauts_df.to_excel(writer, sheet_name='astronauts', index=False)
    mission_df.to_excel(writer, sheet_name='missions', index=False)
