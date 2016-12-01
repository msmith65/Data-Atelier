
#Import Packages
import pandas as pd


#Change Display Settings
pd.set_option("display.max_columns",200)
pd.set_option("display.max_rows",500)


#Load Raw Wealth and Model Data File Filtered By Parameters that give Ana Gloria at least 50 prospects
Model_Filtered = pd.read_excel('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\All Screened Prospects3.xlsx')

Model_Filtered_2 =Model_Filtered[(Model_Filtered["RDD"]=="Not Under Management")&
    (Model_Filtered["Gift Capacity Rating"]>=11)&
    (Model_Filtered["Major Gift Score"]>=108)&
    (Model_Filtered["Total Giving"]>=5000)]


#Load RDD Territories 
Territories = pd.read_excel('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Top 50 by Territory\RDD Territory by ZIP Code\Zip to RDD 2.xlsx')

#Rename Column
Model_Filtered_2.rename(columns={"Original ID":"ID"},inplace=True)

# New Comments to Test Pull Request Feature of Github

#Add Territories to Screened Data
With_Territories = pd.merge(Model_Filtered_2,Territories,how='left',left_on='ZIP',right_on='Zip Code')

# Prospect Has Had an Opportunity
Had_Opportunity = pd.read_excel('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\All LG Opportunities2.xlsx')

#Rename Column
Had_Opportunity.rename(columns={"ID#":"ID"},inplace=True)

#Prior MG Prospect
Prior_Prospect = pd.read_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Prior_MG_Prospects.csv')

#Rename Column
Prior_Prospect.rename(columns={"Prospect ID#":"ID"},inplace=True)

#Find Duplicates from Previously Dropped Prospects
Prior_Duplicates = pd.merge(With_Territories,Prior_Prospect,how='inner',left_on="ID",right_on="ID",indicator=True)

#Find Prospects who have had or have an Opportunity 
Existing_Opportunity = pd.merge(With_Territories,Had_Opportunity,how='inner',left_on='ID',right_on='ID',indicator=True)

#List of Dataframes of Prospects to Remove
To_Remove = [Prior_Duplicates,Existing_Opportunity]

#Dataframe of Prospects to Remove Concatinated instead of Joined
Prospects_to_Remove_2 = pd.concat(To_Remove)

#Drop Duplicates
Prospects_to_Remove_3=Prospects_to_Remove_2.drop_duplicates("ID")

#Overlap Between Previously Dropped and Existing Opportunity
Overlap = pd.merge(Prior_Duplicates,Existing_Opportunity,how='inner',left_on="ID",right_on="ID")

#Removing Previously Old Prospects 
New_Prospects = With_Territories[~With_Territories["ID"].isin(Prospects_to_Remove_3["ID"])].sort_values(by="Major Gift Score",ascending=0)

# Old Prospects That Were Removed  
Old_Prospects_Overlap= With_Territories[With_Territories["ID"].isin(Prospects_to_Remove_3["ID"])]

# Old Prospects That Were Removed - DeDuped
Old_Prospects_Overlap_Dedupe= With_Territories[With_Territories["ID"].isin(Prospects_to_Remove_3["ID"])].drop_duplicates("ID")

#Making Sure the Merge Worked as Expected
Merge_Check = Old_Prospects_Overlap[~Old_Prospects_Overlap["ID"].isin(Prospects_to_Remove_3["ID"])]

#Group New Prospects and write to CSV

Select_Columns = New_Prospects[["ID","Associated Solicitor Code","Major Gift Score"]]

Select_Columns=Select_Columns.rename(columns={"Associated Solicitor Code":"Primary Sol Code"})

Select_Columns=Select_Columns.assign(Opp_Type="LG",Stage=2)

Grouped = Select_Columns.groupby("Primary Sol Code")

# Groups to Dataframes

BN = Grouped.get_group("BN")
BN=BN.nlargest(50,"Major Gift Score")

CI = Grouped.get_group("CI")
CI= CI.nlargest(50,"Major Gift Score")

ES = Grouped.get_group("ES")
ES = ES.nlargest(50,"Major Gift Score")

GL = Grouped.get_group("GL")
GL = GL.nlargest(50,"Major Gift Score")

GP = Grouped.get_group("GP")
GP = GP.nlargest(50,"Major Gift Score")

IL = Grouped.get_group("IL")
IL = IL.nlargest(50,"Major Gift Score")

LA = Grouped.get_group("LA")
LA = LA.nlargest(50,"Major Gift Score")

NE = Grouped.get_group("NE")
NE = NE.nlargest(50,"Major Gift Score")

NENY = Grouped.get_group("NE and NY")
NENY = NENY.nlargest(50,"Major Gift Score")

NY = Grouped.get_group("NY")
NY = NY.nlargest(50,"Major Gift Score")

PA = Grouped.get_group("PA")
PA = PA.nlargest(50,"Major Gift Score")

PO = Grouped.get_group("PO")
PO = PO.nlargest(50,"Major Gift Score")

EC_RI = Grouped.get_group("EC and RI")
EC_RI = EC_RI.nlargest(100,"Major Gift Score")

EC = EC_RI.nlargest(20,"Major Gift Score")
EC["Primary Sol Code"]=EC["Primary Sol Code"].map({"EC and RI":"EC"})

RI = EC_RI.nsmallest(80,"Major Gift Score")
RI["Primary Sol Code"]=RI["Primary Sol Code"].map({"EC and RI":"RI"})

SC = Grouped.get_group("SC")
SC = SC.nlargest(50,"Major Gift Score")

SE = Grouped.get_group("SE")
SE = SE.nlargest(50,"Major Gift Score")

SW = Grouped.get_group("SW")
SW = SW.nlargest(50,"Major Gift Score")

WR = Grouped.get_group("WR")
WR = WR.nlargest(50,"Major Gift Score")

NY_Region = NENY 

# Top 50 NYC Region and Random Sample

NY_Region_Top50 = NY_Region[:50]

NY_Region_Random_Jerry = NY_Region_Top50.sample(n=25)

NY_Region_Random_Jerry["Primary Sol Code"]=NY_Region_Random_Jerry["Primary Sol Code"].map({"NE and NY":"NE"})

NY_Region_Random_Mimi = NY_Region_Top50[~NY_Region_Top50["ID"].isin(NY_Region_Random_Jerry["ID"])]

NY_Region_Random_Mimi["Primary Sol Code"]=NY_Region_Random_Mimi["Primary Sol Code"].map({"NE and NY":"NY"})

#Write DataFrames to CSV
New_Prospects.to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\New_Prospects.csv')

Old_Prospects_Overlap.to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Removed_Prospects.csv')

Frames = [BN,CI,ES,GL,GP,IL,LA,NE,NY,PA,PO,EC,RI,SC,SE,SW,WR,NY_Region_Random_Jerry,NY_Region_Random_Mimi]

def save_xls(list_dfs, xls_path):
    writer = pd.ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,'sheet%s' % n)
    writer.save()
    
save_xls(Frames,'S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Prospects_For_Seeding_Sheets_New_Groups.xlsx')
    
pd.concat(Frames).to_excel('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Top 50 List\Prospects_For_Seeding_OneSheet_New_Groups.xlsx')
    