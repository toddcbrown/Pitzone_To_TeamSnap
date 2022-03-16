import pandas as pd
import numpy as np 
from datetime import datetime 

def join_name(x):
  x = x.split(' ')
  x = ''.join(x)
  x = x.replace('-','')
  return x.lower()

df = pd.read_csv('riders.csv')

# REMOVE UNPAID PITZONE RIDERS
df = df.loc[df['NICA Fee'] != False]

# STOP SCRIPT IF NO PAID RIDERS
if len(df) < 1:
  print('No Paid Riders')
  exit()

# RENAME COLUMNS
df.columns = ['Last Name', 'First Name', 'Email Address 1', 'Phone Number 1', 'Home Phone',
       'Gender', 'Grade', 'Address', 'Racing Category', 'Skill Level',
       'Race Plate Number', 'Participation Agreement Signed', 'Media Release',
       'NICA Fee', 'League Fee', 'Parent 1 last name', 'Parent 1 first name',
       'Email Address 2', 'Phone Number 2', 'Parent 1 home phone',
       'Parent 2 last name', 'Parent 2 first name', 'Email Address 3',
       'Phone Number 3', 'Parent 2 home phone']

# CLEAN UP COLUMNS
df['City'] = np.nan
df['State'] = np.nan
df['ZIP/Postal Code'] = np.nan
df['Birthday'] = np.nan
df['Jersey Number'] = np.nan
df['Non-Player (Y/N) '] = 'N'
df['Grade'] = df['Grade'].apply(str)
df['Position'] = df['Grade'] + ' ' + df['Skill Level']
df['Email Address 1 Label'] = df['First Name'] + "'s email"
df['Email Address 2 Label'] = df['Parent 1 first name'] + ' ' +df['Parent 1 last name'] + "'s email"
df['Email Address 3 Label'] = df['Parent 2 first name'] + ' ' +df['Parent 2 last name'] + "'s email"
df['Phone Number 1 Label'] = df['First Name'] + "'s phone"
df['Phone Number 2 Label'] = df['Parent 1 first name'] + ' ' +df['Parent 1 last name'] + "'s phone"
df['Phone Number 3 Label'] = df['Parent 2 first name'] + ' ' +df['Parent 2 last name'] + "'s phone"

# CONVERT COLUMNS TO TEAMSNAP COLUMN NAMES AND POSITION
df = df[['First Name', 'Last Name', 'Email Address 1', 'Email Address 1 Label',
       'Email Address 2', 'Email Address 2 Label', 'Email Address 3',
       'Email Address 3 Label', 'Phone Number 1', 'Phone Number 1 Label',
       'Phone Number 2', 'Phone Number 2 Label', 'Phone Number 3',
       'Phone Number 3 Label', 'Address', 'City', 'State', 'ZIP/Postal Code',
       'Gender', 'Birthday', 'Jersey Number', 'Position', 'Non-Player (Y/N) ']]


# REMOVE DUPLICATE RECORDS AND CREATE FILE
try:
  teamsnap = pd.read_csv('teamsnapexport.csv')
  
  sample = []
  for i in teamsnap.index:
    sample.append(join_name(teamsnap['First'][i]+teamsnap['Last'][i]))
  Name = []
  for i in df.index:
    Name.append(join_name(df['First Name'][i]+df['Last Name'][i]))
  
  df['Name'] = Name
  df = df[~df['Name'].isin(sample)]
  df = df.drop(['Name'],axis=1)
  df.to_csv( 'Import_to_teamsnap_%s.csv'%datetime.today().strftime('%Y-%m-%d'),index=False)
  for i in df['First Name']:
    print('New Rider',i)
  print(str(len(df))+ ' records to import')
except:
  print('no comparison TeamSnap file to remove duplicates file \n File contains ALL players ')
  df.to_csv( 'Import_to_teamsnap_%s.csv'%datetime.today().strftime('%Y-%m-%d'),index=False)
  