
import pandas as pd
import numpy as np
import os















# Miscellaneous Prep Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

''''''''''''''''''''
'                  '
' Helper Functions '
'                  '
''''''''''''''''''''



def missing_zero_values_table(df):
    
    '''This function will look at any data set and report back on zeros and nulls for every column while also giving percentages of total values
        and also the data types. The message prints out the shape of the data frame and also tells you how many columns have nulls '''
    
    
    
    zero_val = (df == 0.00).astype(int).sum(axis=0)
    null_count = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mz_table = pd.concat([zero_val, null_count, mis_val_percent], axis=1)
    mz_table = mz_table.rename(
    columns = {0 : 'Zero Values', 1 : 'null_count', 2 : '% of Total Values'})
    mz_table['Total Zeroes + Null Values'] = mz_table['Zero Values'] + mz_table['null_count']
    mz_table['% Total Zero + Null Values'] = 100 * mz_table['Total Zeroes + Null Values'] / len(df)
    mz_table['Data Type'] = df.dtypes
    mz_table = mz_table[
        mz_table.iloc[:,1] >= 0].sort_values(
        '% of Total Values', ascending=False).round(1)
    print ("Your selected dataframe has " + str(df.shape[1]) + " columns and " + str(df.shape[0]) + " Rows.\n"      
            "There are " +  str((mz_table['null_count'] != 0).sum()) +
          " columns that have NULL values.")
#         mz_table.to_excel('D:/sampledata/missing_and_zero_values.xlsx', freeze_panes=(1,0), index = False)

    return mz_table


def reduce_equip_cols(df):
    '''
    This function takes in the equipemnet rail data frame and drops collumns:
        - With 80% of null values
        - Features not inlcuded in this analyis
        - Duplicated information columns

    It returns a single dataframe
    '''

    #Drop cols with 80% or more missing values
    df = df.dropna(axis=1, thresh=threshold)

    df = df[['IYR','IMO','RAILROAD','YEAR','MONTH','DAY','TIMEHR','TIMEMIN','AMPM','TYPE','STATE','TEMP','VISIBLTY','WEATHER',
            'TRNSPD','TYPSPD','TRNNBR','TRNDIR','TONS','TYPEQ','TRKNAME','TYPTRK','HEADEND1','LOADF1','LOADP1','EMPTYF1',
            'EMPTYP1','EQPDMG','TRKDMG','CAUSE','CASKLDRR','CASINJRR','CASKLD','CASINJ','HIGHSPD','ACCDMG','STCNTY','TOTINJ',
            'TOTKLD','ENGRS','FIREMEN','CONDUCTR','BRAKEMEN','REGION','TYPRR','NARRLEN','RREMPKLD','RREMPINJ','PASSKLD','PASSINJ',
            'OTHERKLD','OTHERINJ','COUNTY','CNTYCD','PASSTRN','SSB1','NARR1','NARR2','Latitude','Longitud','SIGNAL']]

    return df