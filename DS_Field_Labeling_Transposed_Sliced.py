# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 12:53:39 2016

@author: charles.wiles
"""

import pandas as pd

Labeled_Data = pd.read_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Wealth Screen and Model Returns\May_2016_TotalScreenReturn_wheaders_womodels.csv')

Transposed_Data = Labeled_Data.T

Transposed_Sliced = Transposed_Data.rename(columns={})

Labels1 = Transposed_Sliced.iloc[:,0:2]

Labels2 = Labels1.drop(["Clearview  ID","Search Date","First Name","Middle Name","Last Name","Suffix","Address","City","STATE",
                        "ZIP","2nd Person Last Name","2nd Person First Name","2nd Person Middle Name"])

Labels2.to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Wealth Screen and Model Returns\May_2016_TotalScreenReturn_labels.csv',header=None)