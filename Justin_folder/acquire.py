import pandas as pd
import numpy as np
import rail_data

#~~~~~~~~~~~~~~~~~~~~~~~~Acquire Functions~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_hwyrail():
    
    '''This function acquires the hwy rail accident data, concats all of the dataframes into one'''
    
    df = pd.read_csv('../rail_data/hwy_rail_accidents_2012.csv', index_col=False)
    df1 = pd.read_csv('../rail_data/hwy_rail_accidents_2013.csv', index_col=False)  
    df2 = pd.read_csv('../rail_data/hwy_rail_accidents_2014.csv', index_col=False)  
    df3 = pd.read_csv('../rail_data/hwy_rail_accidents_2015.csv', index_col=False)  
    df4 = pd.read_csv('../rail_data/hwy_rail_accidents_2016.csv', index_col=False)  
    df5 = pd.read_csv('../rail_data/hwy_rail_accidents_2017.csv', index_col=False)  
    df6 = pd.read_csv('../rail_data/hwy_rail_accidents_2018.csv', index_col=False)  
    df7 = pd.read_csv('../rail_data/hwy_rail_accidents_2019.csv', index_col=False)  
    df8 = pd.read_csv('../rail_data/hwy_rail_accidents_2020.csv', index_col=False) 
    
    big_df = pd.concat([df, df1, df2, df3, df4, df5, df6, df7, df8])
    
    return big_df


def get_equiprail():
    
    '''This function acquires the equipment rail accident data, concats all of the dataframes into one'''
    
    
    df = pd.read_csv('../rail_data/rail_equip_accidents_2012.csv', index_col=False)
    df1 = pd.read_csv('../rail_data/rail_equip_accidents_2013.csv', index_col=False)  
    df2 = pd.read_csv('../rail_data/rail_equip_accidents_2014.csv', index_col=False)  
    df3 = pd.read_csv('../rail_data/rail_equip_accidents_2015.csv', index_col=False)  
    df4 = pd.read_csv('../rail_data/rail_equip_accidents_2016.csv', index_col=False)  
    df5 = pd.read_csv('../rail_data/rail_equip_accidents_2017.csv', index_col=False)  
    df6 = pd.read_csv('../rail_data/rail_equip_accidents_2018.csv', index_col=False)  
    df7 = pd.read_csv('../rail_data/rail_equip_accidents_2019.csv', index_col=False)  
    df8 = pd.read_csv('../rail_data/rail_equip_accidents_2020.csv', index_col=False) 
    
    equip_df = pd.concat([df, df1, df2, df3, df4, df5, df6, df7, df8])
    
    return equip_df
    