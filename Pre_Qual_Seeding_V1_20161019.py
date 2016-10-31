
#Import Packages
import pandas as pd
import numpy as np
import sklearn as sk

#Change Display Settings
pd.set_option("display.max_columns",200)
pd.set_option("display.max_rows",500)


#Load Raw Wealth and Model Data File Filtered By Parameters that give Ana Gloria at least 50 prospects
Model_Filtered = pd.read_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\All Screened Prospects.csv',low_memory=False)

#Rename Column
Model_Filtered.rename(columns={"Original ID":"ID"},inplace=True)

# Prospect Has Had an Opportunity
Had_Opportunity = pd.read_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\All LG Opportunities.csv',low_memory=False)

#Rename Column
Had_Opportunity.rename(columns={"ID#":"ID"},inplace=True)

#Prior MG Prospect
Prior_Prospect = pd.read_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Prior_MG_Prospects.csv',low_memory=False)

#Rename Column
Prior_Prospect.rename(columns={"Prospect ID#":"ID"},inplace=True)

#Find Duplicates from Previously Dropped Prospects
Prior_Duplicates = pd.merge(Model_Filtered,Prior_Prospect,how='inner',left_on="ID",right_on="ID",indicator=True)

#Find Prospects who have had or have an Opportunity 
Existing_Opportunity = pd.merge(Model_Filtered,Had_Opportunity,how='inner',left_on="ID",right_on="ID",indicator=True)

#List of Dataframes of Prospects to Remove
To_Remove = [Prior_Duplicates,Existing_Opportunity]

#Dataframe of Prospects to Remove
Prospects_to_Remove = pd.merge(Prior_Duplicates,Existing_Opportunity,how="outer",left_on="ID",right_on="ID")

#Dataframe of Prospects to Remove Concatinated instead of Joined
Prospects_to_Remove_2 = pd.concat(To_Remove)

#Drop Duplicates
Prospects_to_Remove_3=Prospects_to_Remove_2.drop_duplicates("ID")

#Overlap Between Previously Dropped and Existing Opportunity
Overlap = pd.merge(Prior_Duplicates,Existing_Opportunity,how='inner',left_on="ID",right_on="ID")

#Removing Previously Old Prospects 
New_Prospects = Model_Filtered[~Model_Filtered["ID"].isin(Prospects_to_Remove["ID"])]

#Old Prospects That Were Removed  
Old_Prospects_Overlap = Model_Filtered[Model_Filtered["ID"].isin(Prospects_to_Remove["ID"])]

#Making Sure the Merge Worked as Expected
Merge_Check = Old_Prospects_Overlap[~Old_Prospects_Overlap["ID"].isin(Prospects_to_Remove_3["ID"])]


#Group New Prospects and write to CSV
New_Prospects.groupby(["Zip Code (group)","Gift Capacity Rating","State", "ZIP","Major Gift Score","ID"]).size().to_frame().to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Grouped.csv')

#Writing New Prospects to CSV
New_Prospects.to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\New_Prospects.csv')

#Writing Old Prospects That Were Removed to CSV
Old_Prospects_Overlap.to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Removed_Prospects.csv')




