import pandas as pd
import numpy as np
import os
import sys
import json
from typing import Dict, List, Optional, Union, cast
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import unicodedata
import re

from acquire import get_hwyrail, get_equiprail


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
            'EMPTYP1','EQPDMG','TRKDMG','CAUSE','CASKLD','CASINJ','HIGHSPD','ACCDMG','ENGRS','CONDUCTR',
            'BRAKEMEN','REGION','TYPRR', 'Latitude','Longitud','SIGNAL']]

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
                   'total_killed', 
                   'total_injured', 
                   'max_speed', 
                   'total_damage', 
                   'engineers_onduty',
                   'conductors_onduty', 
                   'brakemen_onduty', 
                   'region', 
                   'typrr', 
                   'lat', 
                   'long', 
                   'signal_type',
                   'date']
    
    return df


def drop_under_represented_rr(df): 
    '''
    This function takes in a railroad accident data frame
    and drops any observations representing railroad companies
    where the railroad company has less than 300 accidents in the dataframe
    
    It returns a single dataframe
    '''
    
    #Define the value counts for railroad_company in the dataframe
    value_counts = df['railroad_company'].value_counts()
    
    #Select the observations to remove based on railroad_company count representation threshold
    to_remove = value_counts[value_counts < 300].index
    
    # Keep rows where the railroad_company column is not in to_remove if n was defined
    if 300 > 0:
        df = df[~df.railroad_company.isin(to_remove)]
    else: 
        df = df 
        
    return df


#create seasons based on month in a date column

def get_season(row):
    
    '''This function takes in the date column and returns a string containing a season name. A new 
    season column can be created using this column.'''
    
    if row['date'].month >= 3 and row['date'].month <= 5:
        return 'Spring'
    elif row['date'].month >= 6 and row['date'].month <= 8:
        return 'Summer'
    elif row['date'].month >= 9 and row['date'].month <= 11:
        return 'Fall'
    else:
        return 'Winter'


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

    #Drop underrepresented railroad companies in dataframe
    df = drop_under_represented_rr(df)
    
    #Create season column
    df['season'] = df.apply(get_season, axis=1)

    #Read fips_state_csv to df for state abbreviation
    fips_df = pd.read_csv('fips_state_key.csv', usecols=[1,2])

    #Mege state to df
    df = df.merge(fips_df, how='inner', left_on='state', right_on='state', right_index=True)

    #Rename state cols
    df.rename(columns={'state': 'state_fips', ' stusps': 'state'}, inplace=True)
    
    #Create year column
    df['year'] = df['date'].dt.year
    
    return df

############################################################################################################################

''''''''''''''''''''
'                  '
'  Hwy Prep  '
'    Functions     '
''''''''''''''''''''


def min_reduce_hwy_cols(df):
    '''
    This function takes in the hwy/rail data frame and drops columns:
        - With 80% of null values
        - Features not inlcuded in this analyis
        - Duplicated information columns

    It returns a single dataframe
    '''
    #Define threshold
    threshold = len(df) * 0.80
    
    #Drop cols with 80% or more missing values
    df = df.dropna(axis=1, thresh=threshold)

    df = df[['RAILROAD','INCDTNO','YEAR','MONTH','DAY','TIMEHR','TIMEMIN','AMPM','STATION','COUNTY','STATE','REGION','CITY',
 'VEHSPD','TYPVEH','VEHDIR','POSITION','TYPACC','HAZARD','TEMP','VISIBLTY','WEATHER','TYPEQ','TYPTRK','NBRLOCOS','NBRCARS',
 'TRNSPD','TRNDIR','LOCWARN','WARNSIG','LIGHTS','STANDVEH','TRAIN2','MOTORIST','VIEW','VEHDMG','DRIVER','INVEH','TOTKLD',
 'TOTINJ','TOTOCC','PUBLIC','CNTYCD','WHISBAN','DRIVAGE','DRIVGEN',
 'PLEONTRN','USERKLD','USERINJ','RREMPKLD','RREMPINJ','PASSKLD','PASSINJ','ROADCOND']]

    return df


def max_reduce_hwy_cols(df):
    '''
    This function takes in the equipemnet rail data frame and drops collumns:
        - With 60% of null values
        - Features not inlcuded in this analyis
        - Duplicated information columns

    It returns a single dataframe
    '''
    #Define threshold
    threshold = len(df) * 0.60
    
    #Drop cols with 80% or more missing values
    df = df.dropna(axis=1, thresh=threshold)

    df = df[['RAILROAD','INCDTNO','YEAR','MONTH','DAY','TIMEHR','TIMEMIN','AMPM','STATION','COUNTY','STATE','REGION','CITY',
 'VEHSPD','TYPVEH','VEHDIR','POSITION','TYPACC','HAZARD','TEMP','VISIBLTY','WEATHER','TYPEQ','TYPTRK','NBRLOCOS','NBRCARS',
 'TRNSPD','TRNDIR','LOCWARN','WARNSIG','LIGHTS','STANDVEH','TRAIN2','MOTORIST','VIEW','VEHDMG','DRIVER','INVEH','TOTKLD',
 'TOTINJ','TOTOCC','PUBLIC','CNTYCD','WHISBAN','DRIVAGE','DRIVGEN',
 'PLEONTRN','USERKLD','USERINJ','RREMPKLD','RREMPINJ','PASSKLD','PASSINJ','ROADCOND']]

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

def general_hwy_clean(df):
    '''
    This function takes in the equip df and prepares it for analysis by:
        - lowercasing all column titles
        - convert lat and long to string dtypes
        -

    It returns a single dataframe
        
    '''
    #lowecase all column titles
    df.columns= df.columns.str.lower()

    #Drop null values
    #drop null values
    df = df.dropna(axis=0)

    return df

def set_hwy_index(df):
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


def rename_hwy_columns(df):
    
    '''
    This function will rename the columns. Only run after max_reduce, concat_date_time, general_equip_clean,
    and set_equip_index
    
    '''  
    
    #rename columns
    
    df.columns = ['railroad_company',
                  'station',
                  'county',
                  'state',
                  'region',
                  'city',
                  'vehicle_speed',
                  'vehicle_type',
                  'vehicle_direction',
                  'position',
                  'accident_type',
                  'hazmat_entity',
                  'temp',
                  'visibility',
                  'weather',
                  'train_type',
                  'track_type',
                  'front_engines',
                  'railcar_quantity',
                  'train_speed',
                  'train_direction',
                  'warning_location',
                  'warning_signal',
                  'lights',
                  'standveh',
                  'other_train',
                  'motorist_action',
                  'view_obstruction',
                  'vehicle_damage',
                  'driver_fate',
                  'vehicle_occupied',
                  'total_killed',
                  'total_injured',
                  'vehicle_occupants',
                  'ispublic_crossing',
                  'fips',
                  'whistle_ban',
                  'driver_age',
                  'driver_gender',
                  'train_occupants',
                  'user_killed',
                  'user_injured',
                  'rail_killed',
                  'rail_injured',
                  'train_pass_killed',
                  'train_pass_injured',
                  'road_condtions',
                  'date']
    
    return df

def prep_hwy_df(df):
    '''
    This function takes in the equipment rail data frame
    and applies the prepare and cleaning functions to it so that it is ready
    for analysis.

    It returns a single dataframe
    '''

        
    #Reduce columns
    df = max_reduce_hwy_cols(df)

    #Deal with date time columsn
    df = concat_date_time(df)

    #general cleaning
    df = general_hwy_clean(df)

    #set the index
    df = set_hwy_index(df)

    #rename columns
    df = rename_hwy_columns(df)
    
    #Drop underrepresented railroad companies in dataframe
    df = drop_under_represented_rr(df)
    
    #Create season column
    df['season'] = df.apply(get_season, axis=1)
    
    #Read fips_state_csv to df for state abbreviation
    fips_df = pd.read_csv('fips_state_key.csv', usecols=[1,2])

    #Mege state to df
    df = df.merge(fips_df, how='inner', left_on='state', right_on='state', right_index=True)

    #Rename state cols
    df.rename(columns={'state': 'state_fips', ' stusps': 'state'}, inplace=True)

    #Create year column
    df['year'] = df['date'].dt.year
    
    #Fix left aligned numbers
    df['lights'] = df['lights'].apply(int)
    df['weather'] = df['weather'].apply(int)
    
    hazindex = df.loc[df['hazmat_entity'].isin([' '])].index
    df.drop(hazindex, inplace=True)
    df['hazmat_entity'] = df['hazmat_entity'].apply(int)
    
    # fix driver gender
    df['driver_gender'] = df.driver_gender.replace(' ', 1)
    df['driver_gender'] = df['driver_gender'].apply(int)
    gendindex = df.loc[df['driver_gender'].isin(['u'])].index
    df.drop(gendindex, inplace=True)
    
    
    return df



############################################################################################################################

''''''''''''''''''''
'                  '
'   NLP Prep       '
'    Function      '
''''''''''''''''''''


def equip_nlp():
    
    ''' This function takes in a dataframe and returns a df that is ready for NLP exploration'''
    
    
    df = get_equiprail()
    
    counts = df['RAILROAD'].value_counts()

    newdf = df[~df['RAILROAD'].isin(counts[counts < 400].index)]
    
    #create dataframe of just railroad and narratives
    df = newdf[['RAILROAD','NARR1','NARR2','NARR3','NARR4','NARR5', 'NARR6','NARR7','NARR8','NARR9','NARR10',
               'NARR11','NARR12','NARR13','NARR14','NARR15']]
    
    #replace NaN with empty string spaces

    df = df.replace(np.nan, '', regex=True)
    
    #merge all narrative columns into 1 single column

    df["narrative"] = df["NARR1"] + df["NARR2"] + df["NARR3"] + df["NARR4"] + df["NARR5"] + df["NARR6"] + df["NARR7"] +           df["NARR8"] + df["NARR9"] + df["NARR10"] + df["NARR11"] + df["NARR12"] + df["NARR13"] + df["NARR14"] + df["NARR15"]
    
    #drop unneeded narrative columns as they have already been merged

    df = df.drop(['NARR1', 'NARR2', 'NARR3', 'NARR4', 'NARR5', 'NARR6','NARR7','NARR8','NARR9','NARR10',
               'NARR11','NARR12','NARR13','NARR14','NARR15'], axis=1)
    
    #find narratives with nulls
    null_narrative = df[df['narrative'].isnull()].index
    
    #drop any null narratives
    df.drop(null_narrative , inplace=True)
    
    return df