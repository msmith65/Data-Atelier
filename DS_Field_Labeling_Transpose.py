# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 12:53:39 2016

@author: charles.wiles
"""

import pandas as pd

Labeled_Data = pd.read_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Wealth Screen and Model Returns\May_2016_TotalScreenReturn_wheaders_womodels.csv')

Transposed_Data = Labeled_Data.T

Transposed_Sliced = Transposed_Data.rename(columns={})

Transposed_Sliced.to_csv('S:\CG ANALYTICS\Wealth Screening\WealthEngine\May 2016 Screening Return\Wealth Screen and Model Returns\May_2016_TotalScreenReturn_wheaders_womodels_transposed.csv',header=None)