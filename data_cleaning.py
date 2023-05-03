import pandas as pd
import numpy as np
import re

#Load the data into a pandas DataFrame:
df = pd.read_excel('./Total.xlsx')

#Drop the unnecessary columns:
df.drop(['Recommendations', 'Featured', 'Interests'], axis=1, inplace=True)

#Clean the 'Experience' column by extracting the start and end years and calculating the total experience in years:
def calculate_experience(years):
    if pd.isna(years):
        return np.nan
    years = re.findall(r'\d{4}', years)
    if len(years) == 2:
        return int(years[1]) - int(years[0])
    else:
        return np.nan

df['Experience'] = df['Experience'].apply(calculate_experience)

#Clean the 'Education' column by extracting the start and end years and calculating the total education in years:
def calculate_education(years):
    if pd.isna(years):
        return np.nan
    years = re.findall(r'\d{4}', years)
    if len(years) == 2:
        return int(years[1]) - int(years[0])
    else:
        return np.nan

df['Education'] = df['Education'].apply(calculate_education)

#Clean the 'Licenses & certifications' column by removing unnecessary characters:
def clean_licenses(certifications):
    if pd.isna(certifications):
        return np.nan
    certifications = re.sub(r'\([^)]*\)', '', certifications)
    return certifications.strip()

df['Licenses & certifications'] = df['Licenses & certifications'].apply(clean_licenses)

#Clean the 'Skills' column by removing unnecessary characters and splitting the text into a list:
def clean_skills(skills):
    if pd.isna(skills):
        return []
    skills = re.sub(r'[^\w\s]+', '', skills)
    return skills.lower().split()

df['Skills'] = df['Skills'].apply(clean_skills)

#Replace missing values with NaN:
df.replace({'': np.nan, ' ': np.nan, '-': np.nan}, inplace=True)

#Drop rows with missing values:
df.dropna(inplace=True)

#Reset the index:
df.reset_index(drop=True, inplace=True)

# Save the cleaned data to a new Excel file
df.to_excel('cleaned_profiles.xlsx', index=False)