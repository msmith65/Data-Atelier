
#Import Packages
import pandas as pd


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
New_Prospects = Model_Filtered[~Model_Filtered["ID"].isin(Prospects_to_Remove["ID"])].sort_values(by="Major Gift Score",ascending=0)

# Old Prospects That Were Removed  
Old_Prospects_Overlap= Model_Filtered[Model_Filtered["ID"].isin(Prospects_to_Remove["ID"])]

#Making Sure the Merge Worked as Expected
Merge_Check = Old_Prospects_Overlap[~Old_Prospects_Overlap["ID"].isin(Prospects_to_Remove_3["ID"])]

#Group New Prospects and write to CSV
Grouped = New_Prospects.groupby(["Zip Code (group)"])

# Groups to Dataframes

BN = Grouped.get_group("BN")

ES = Grouped.get_group("ES")

GL = Grouped.get_group("GL")

GP = Grouped.get_group("GP")

IL = Grouped.get_group("IL")

MA = Grouped.get_group("MA")

NE = Grouped.get_group("NE")

NENY = Grouped.get_group("NE and NY")

NW = Grouped.get_group("NW")

NY = Grouped.get_group("NY")

PA = Grouped.get_group("PA")

PO = Grouped.get_group("PO")

RI = Grouped.get_group("RI")

SC = Grouped.get_group("SC")

SE = Grouped.get_group("SE")

SO = Grouped.get_group("SO")

SW = Grouped.get_group("SW")

WR = Grouped.get_group("WR")

NY_Regions = [NE,NY,NENY] 

NY_Region =pd.concat(NY_Regions)

# Top 100 NYC Region and Random Sample

NY_Region_Top100 = NY_Region[:100]

NY_Region_Random_Jerry = NY_Region_Top100.sample(n=50)

NY_Region_Random_Mimi = NY_Region_Top100[~NY_Region_Top100["ID"].isin(NY_Region_Random_Jerry["ID"])]

#Write DataFrames to CSV
New_Prospects.to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\New_Prospects.csv')

Old_Prospects_Overlap.to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Removed_Prospects.csv')

Frames = [BN,ES,GL,GP,IL,MA,NW,PA,PO,RI,SC,SE,SO,SW,WR,NY_Region_Random_Jerry,NY_Region_Random_Mimi]

def save_xls(list_dfs, xls_path):
    writer = pd.ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n)
    writer.save()
    
save_xls(Frames,'S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Prospects_For_Seeding.xlsx')    
    