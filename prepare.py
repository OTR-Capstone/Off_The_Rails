
import pandas as pd
import numpy as np
import os
from env import sys


# Miscellaneous Prep Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

''''''''''''''''''''
'                  '
' Helper Functions '
'                  '
''''''''''''''''''''



def missing_zero_values_table(df):
    
    '''
    This function will look at any data set and report back on zeros and nulls for every column 
    while also giving percentages of total values and also the data types. 
    The message prints out the shape of the data frame and also tells you how many columns have nulls 
    '''
    
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

    

############################################################################################################################

''''''''''''''''''''
'                  '
'  Equipment Prep  '
'    Functions     '
''''''''''''''''''''



def min_reduce_equip_cols(df):
    '''
    This function takes in the equipemnet rail data frame and drops collumns:
        - With 80% of null values
        - Features not inlcuded in this analyis
        - Duplicated information columns

    It returns a single dataframe
    '''
    #Define threshold
    threshold = len(df) * 0.80
    
    #Drop cols with 80% or more missing values
    df = df.dropna(axis=1, thresh=threshold)

    df = df[['IYR','IMO','RAILROAD','YEAR','MONTH','DAY','TIMEHR','TIMEMIN','AMPM','TYPE','STATE','TEMP','VISIBLTY','WEATHER',
            'TRNSPD','TYPSPD','TRNDIR','TONS','TYPEQ','TYPTRK','HEADEND1','LOADF1','LOADP1','EMPTYF1',
            'EMPTYP1','EQPDMG','TRKDMG','CAUSE','CASKLDRR','CASINJRR','CASKLD','CASINJ','HIGHSPD','ACCDMG','TOTINJ',
            'TOTKLD','ENGRS','FIREMEN','CONDUCTR','BRAKEMEN','REGION','TYPRR','NARRLEN','RREMPKLD','RREMPINJ','PASSKLD','PASSINJ',
            'OTHERKLD','OTHERINJ','COUNTY','CNTYCD','PASSTRN','NARR1','NARR2','Latitude','Longitud','SIGNAL']]

    return df



def max_reduce_equip_cols(df):
    '''
    This function takes in the equipemnet rail data frame and drops collumns:
        - With 80% of null values
        - Features not inlcuded in this analyis
        - Duplicated information columns

    It returns a single dataframe
    '''
    #Define threshold
    threshold = len(df) * 0.60
    
    #Drop cols with 80% or more missing values
    df = df.dropna(axis=1, thresh=threshold)

    df = df[['INCDTNO','RAILROAD','YEAR','MONTH','DAY','TIMEHR','TIMEMIN','AMPM','TYPE','STATE','TEMP','VISIBLTY','WEATHER',
            'TRNSPD','TRNDIR','TONS','TYPEQ','TYPTRK','HEADEND1','LOADF1','LOADP1','EMPTYF1',
            'EMPTYP1','EQPDMG','TRKDMG','CAUSE','CASKLDRR','CASINJRR','CASKLD','CASINJ','HIGHSPD','ACCDMG','ENGRS','CONDUCTR',
            'BRAKEMEN','REGION','TYPRR','RREMPKLD','RREMPINJ','PASSKLD','PASSINJ',
            'PASSTRN','Latitude','Longitud','SIGNAL']]

    return df




def concat_date_time(df):
    '''
    This function takes in the equip rail data frame and:
    - Concatenates the date time values as a datetime object
    - Drops the original columns for date and time
        
    It returns a single dataframe
    
    '''
    
    #Concatenate datetime columns
    df['date'] = pd.to_datetime(df.MONTH.astype(str)+' '+df.DAY.astype(str)+' '+df.YEAR.astype(str)+' '+df.TIMEHR.astype(str)+':'+df.TIMEMIN.astype(str)+' '+df.AMPM.astype(str))
    
    #Drop original date time columns
    df.drop(columns={'YEAR', 'MONTH', 'DAY', 'TIMEHR', 'TIMEMIN', 'AMPM'}, inplace=True)
    
    return df





def general_equip_clean(df):
    '''
    This function takes in the equip df and prepares it for analysis by:
        - lowercasing all column titles
        - convert lat and long to string dtypes
        -

    It returns a single dataframe
        
    '''
    #lowecase all column titles
    df.columns= df.columns.str.lower()

    #Convert lat and long to strings
    df.latitude = df.latitude.astype(str)
    df.longitud = df.longitud.astype(str)

    #Drop null values
    #drop null values
    df = df.dropna(axis=0)

    return df




def set_equip_index(df):
    '''
    This function takes in the equipment dataframe and sets the index
    to the unique incident number after first dropping the observations
    with duplicate incident numbers
    '''

    #Filters out observations with unique incident numbers 
    counts = df['incdtno'].value_counts()
    df = df[~df['incdtno'].isin(counts[counts > 1].index)]

    #set the index
    df.set_index('incdtno', drop=True, inplace=True)

    return df

def rename_columns(df):
    
    '''
    This function will rename the columns. Only run after max_reduce, concat_date_time, general_equip_clean,
    and set_equip_index
    
    '''  
    
    #rename columns
    
    df.columns = ['railroad_company', 
                   'accident_type', 
                   'state', 
                   'temp', 
                   'visibility',
                   'weather', 
                   'train_speed', 
                   'train_direction',
                   'train_weight', 
                   'train_type',
                   'track_type', 
                   'front_engines', 
                   'loadfrght_cars',
                   'loadpass_cars', 
                   'emptyfrght_cars',
                   'emptypass_cars', 
                   'equip_damage',
                   'track_damage', 
                   'cause',
                   'caskldrr',
                   'casinjrr', 
                   'total_killed', 
                   'total_injured', 
                   'max_speed', 
                   'total_damage', 
                   'engineers_onduty',
                   'conductors_onduty', 
                   'brakemen_onduty', 
                   'region', 
                   'typrr', 
                   'rremp_killed',
                   'rremp_injured',
                   'passengers_killed',
                   'passengers_injured',
                   'passtrn', 
                   'lat', 
                   'long', 
                   'signal_type',
                   'date']


def prep_equip_df(df):
    '''
    This function takes in the equipment rail data frame
    and applies the prepare and cleaning functions to it so that it is ready
    for analysis.

    It returns a single dataframe
    '''

    #Reduce columns
    df = max_reduce_equip_cols(df)

    #Deal with date time columsn
    df = concat_date_time(df)

    #general cleaning
    df = general_equip_clean(df)

    #set the index
    df = set_equip_index(df)

    #rename columns
    df = rename_columns(df)
    
    return df
