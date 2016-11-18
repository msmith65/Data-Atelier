# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:00:38 2016

@author: charles.wiles
"""

import pandas as pd

#Read in Files 
Research_Codes = pd.read_excel('C:\Users\charles.wiles\Desktop\Research Category Codes.xls')

Screened_Prospects = pd.read_csv('P:\Nicolette Linehan\May_2016_TotalScreenReturn_with_model.csv', low_memory=False)

#Select WE Codes
WE_Codes = Research_Codes[Research_Codes["Research Source Code"]=="WE"].set_index('Research Category Code')


New_Headers = {'AGE':'WE.GCAGEUSED','P2G Score Combo':'WE.P2GCOMBO','P2G Description':'WE.P2GDESC',
'P2G Score (first digit)':'WE.P2GSCORE','P2G Score (second digit)':'WE.P2GSCORE2','Total Assets':'WE.ASSETRANGE',
'Total Asset Rating':'WE.ASSETRATING','Net Worth':'WE.NETWORTHRANGE','Net Worth Rating':'WE.NETWORTHRATING',
'Cash on Hand':'WE.LIQUIDITYRANGE','Cash on Hand Rating':'WE.LIQUIDITYRATING','Estimated Annual Donations':'WE.EADRANGE',
'Est. Annual Donations Rating':'WE.EADRATING','Gift Capacity Range':'WE.GIVINGCAPACITYRANGE','Gift Capacity Rating':'WE.GIVINGCAPACITYRATING',
'Gift Capacity - Income':'WE.GCINCOMERANGE','Gift Capacity - Real Estate':'WE.GCREALESTATERANGE','Gift Capacity - Stock':'WE.GCSTOCKSRANGE',
'Gift Capacity - Pension':'WE.GCPENSIONRATING','Gift Capacity - Donations':'WE.GCGIVINGUSED','Estimated Gift Capacity':'WE.CAPACITY',
'Influence Rating':'WE.INFLUENCERATING','Inclination: Affiliation':'WE.INCLINATIONAFF','Inclination: Giving':'WE.INCLINATIONGIV',
'Bequest':'WE.BEQUEST','Annuity':'WE.ANNUITY','Trust':'WE.TRUST','Income':'WE.INCOMERANGE','Income Rating':'WE.INCOMERATING',
'Pension':'WE.PENSIONSRANGE','Pension Rating':'WE.PENSIONSRATING','Real Estate Value':'WE.GCREALESTATEUSED','Real Estate Value Rating':'WE.REALESTATEVALUERATING',
'Real Estate Properties':'WE.REALESTATECOUNT','Stock Direct Holdings':'WE.DIRECTSTOCKRANGE','Stock Direct Holdings Rating':'WE.DIRECTSTOCKRATING',
'Stock Total Value':'WE.TOTALSTOCKRANGE','Stock Total Value Rating':'WE.TOTALSTOCKRATING','Charitable Donations':'WE.NPOGIVERANGE','Charitable Donations Rating':'WE.NPOGIVERATING',
'Political Donations':'WE.POLTOTRANGE','Political Donations Rating':'WE.POLTOTRATING','Total Donations':'WE.DONTOTRANGE','Total Donations Rating':'WE.DONTOTRATING',
'Business Ownership':'WE.DBCOMPANYVALUERANGE','Co. Ownership Value Rating':'WE.DBCOMPANYVALUERATING','Co. Sales Volume':'WE.BSNSSALESVOLUMERANGE',
'Co. Sales Volume Rating':'WE.BSNSSALESVOLRATING', 'Aircraft Owner':'WE.AIRCRAFTOWNER','Boat Owner':'WE.BOATOWNER','Inner Circle Match':'WE.ICMATCHFLAG',
'Inner Circle Member':'WE.ICFLAG','Major Donor':'WE.CDQOM','Board Member':'WE.BOARDMEMBER','QOM - Aircraft':'WE.AIRQOM2','QOM - Airmen':'WE.AMENQOM2',
'QOM - DnB':'WE.DBQOM2','QOM - Vols and Dirs':'WE.GSQOM2','QOM - Do Not Mail':'WE.DNMQOM2','QOM - Charitable Donations':'WE.DONQOM2','QOM - Fed Election Campaign':'WE.FECQOM2',
'QOM - GuideStar Foundation':'WE.GSFDNQOM2','QOM - GuideStar Directors':'WE.GSQOM2','QOM - Household Profile':'WE.HPROFQOM2','QOM - Hoovers':'WE.HVRQOM2','QOM - Major Donor':'WE.MDQOM2',
'QOM - Physicians Profile':'WE.MEDQOM2','QOM - Market Guide':'WE.MGQOM2', 'QOM - Section 527 Directors':'WE.PDIRQOM2', 'QOM - Section 527 Pol. Org':'WE.POLOQOM2',
'QOM - Pension':'WE.PENQOM2','QOM - Philanthropic Donations':'WE.PHILQOM2','QOM - Real Estate':'WE.REALESTQOM2','QOM - State Political':'WE.SPDQOM2',
'QOM - SSA Death Index':'WE.SSDMQOM2','QOM - Wealth ID Securities':'WE.STOCKQOM2','QOM -- Foundation Trustees':'WE.TRUSTQOM2','QOM -- Merchant Vessels':'WE.VDSQOM2',
'QOM -- Marquis Whos Who':'WE.WWQOM2', 'Major Gift Model Decile':'MGMD','Major Gift Model Score':'MGMS','Planned Giving Model Decile':'PGMD','Planned Giving Model Score':'PGMS'
}

Screened_Prospects.rename(columns=New_Headers,inplace=True)

#Screened Prospects Column Headers To List
Prospect_Columns = list(Screened_Prospects.columns.values)
 
Column_Headers=pd.Series(Prospect_Columns).to_frame()

Full_Headers= pd.merge(Column_Headers,WE_Codes,how='left',left_on=0,right_index=True)

#Subset List 
Prospect_Columns_2=Prospect_Columns[2:]

Prospect_Columns_3=Prospect_Columns_2[:121]

Prospect_Columns_4=Prospect_Columns_2[171:]

Prospect_Columns_5=Prospect_Columns_3+Prospect_Columns_4

Screened_Prospects_Short =  Screened_Prospects[Prospect_Columns_5]

Prospects_Short_Transposed = Screened_Prospects_Short.T

With_Headers = pd.merge(Prospects_Short_Transposed,Full_Headers,how='left',left_index=True, right_on=0).set_index(0).T

With_Headers.set_index("OriginalID")

With_Headers.to_csv('C:\Users\charles.wiles\Desktop\Headers_5.csv')
