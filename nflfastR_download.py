"""
****** RUN THIS SCRIPT FIRST *******
The download_years function downloads nflfastR data for a specified number of
years. After downloading, it calls the clean_nflfastr_data function to remove
unneeded data--this makes processing the data MUCH faster.

use_list is the list of nflfastR fields you plan to use in the charts. If 
you're expanding on my original files, you will possibly need to edit that
list. Find detailed field descriptions here: 
    https://www.nflfastr.com/articles/field_descriptions.html
"""

import time
import os
import pandas as pd
import numpy as np


def download_years(first_year,last_year):
    # start timer
    t0=time.time()
    
    # check if the raw data directory doesn't exist
    if not os.path.exists("raw_yearly_data"):
        # make directory
        os.makedirs("raw_yearly_data")
    
    # check if the cleaned data directory doesn't exist
    if not os.path.exists("cleaned_data"):
        # make directory
        os.makedirs("cleaned_data")
    
    # initialize stuff
    dl_years = list(range(first_year,last_year + 1))
    dl_data = pd.DataFrame()
    
    # download new data
    for i in dl_years:  
        print(i, "download started")
        
        # PLEASE STOP CHANGING URL'S!!!
        # url = 'https://github.com/nflverse/nflfastR-data/blob/master/data/play_by_play_' + str(i) + '.zip'
        # url = 'https://github.com/guga31bb/nflfastR-data/blob/master/data/play_by_play_' + str(i) + '.csv.gz?raw=True'
        url = 'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_' + str(i) + '.csv.gz'
        dl_data = pd.read_csv(url, compression='gzip', low_memory=False)
        
        # save raw data
        filename = str(i) + '.csv'
        dl_data.to_csv('raw_yearly_data\\' + filename, compression=None, index=False)
        
        # clean the data (will save automatically)
        clean_nflfastr_data(filename)
    
    # stop timer and report
    elapsed = time.time() - t0
    yrs_ct = len(dl_years)
    print('Done.')
    print(f'Downloading/saving {yrs_ct} year(s) took {elapsed:.1f} seconds')
    return

def clean_nflfastr_data(file):
    # initialize some stuff
    filt_data = pd.DataFrame()
    data = pd.DataFrame()
    
    # find all of the fields in the file
    os.chdir("raw_yearly_data")
    all_fields = pd.read_csv(file, nrows=0).columns.tolist()
    
    # list of all the fields you want to use
    use_list = ['passer',
                'game_id',
                'passer_id',
                'posteam',
                'player_id',
                'qb_epa',
                'qb_dropback'
                ]
    
    # determine the fields to be removed
    remove_fields = list(set(all_fields) - set(use_list))
    
    # read .csv
    print(f'cleaning & saving {file}')
    filt_data = pd.read_csv(file, compression=None, low_memory=False)
    
    # remove columns that are not needed 
    filt_data = filt_data.drop(remove_fields, axis=1, errors='ignore')
    
    # save as csv in clean data directory
    os.chdir("..")
    filt_data.to_csv("cleaned_data\\" + file)
    return

if __name__ == '__main__':
    # Specify the range of years to be downloaded (inclusive)
    # Note: nflfastR data goes back to 1999
    # It is updated within 24 hours after the completion of each game
    # (usually within 6 hours)
    download_years(1999,2023)
