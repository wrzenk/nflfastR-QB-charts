"""
This file reads in csv files from nflfastR's dataset (1999-current). Then finds
which passer has the most qb_epa after n games, for n = 1 up to the most games
played. It exports a csv and a .png file. It returns the filtered data and the
table (in dataframes).

For a while I was worried that the qb_epa field didn't include designed qb 
runs, but apparently it does. Definitively confirmed by Josh Allen's week 1 
rush against the Rams in 2022. With 11:35 left in the 3rd quarter, Josh rushed
for 7 yards on 2nd and 9 (row 270 in the 2022.csv). It wasn't a scramble, it
was a run play. And he was credited with 0.148121458943933 qb_epa, so it's not
just passing plays.
"""

import time
import sys
import pandas as pd
import numpy as np
from format_table import df2table

def epa_func(last_year,chart_rows=35):
    # start timer
    t_0=time.time()
    
    # initialize some stuff
    years = list(range(1999,last_year + 1))
    filt_data = pd.DataFrame()
    data = pd.DataFrame()
    
    # read raw data and filter it
    for i in years:  
        sys.stdout.write("\r")
        sys.stdout.write("processing Total EPA for {:2d}".format(i))
        sys.stdout.flush()
        filt_data = pd.read_csv('cleaned_data\\' + str(i) + '.csv', compression=None, low_memory=False)
        filt_data = filt_data.groupby(['passer_id',
                                       'game_id',
                                       'passer',
                                       'posteam'])\
                                        [['passer',
                                          'game_id',
                                          'qb_epa',
                                          'passer_id',
                                          'posteam']].sum().reset_index()
        # combine into one file
        data = pd.concat([data,filt_data])
    
    # sort by game_id, then by passer
    data = data.sort_values(by=['passer_id','game_id']).reset_index(drop=True)
    
    # find how many player-games there are
    data_rows = len(data)
    
    # inialize some stuff
    game_num = np.ones(data_rows)
    j = 0
    
    # create game number data
    for i in data.loc[:,'passer_id']:  
        if j == data_rows - 2:
            break
        if data.loc[j + 1, 'passer_id']==data.loc[j, 'passer_id']:
            game_num[j + 1] = game_num[j] + 1
        j = j + 1
    
    # fix the last row
    if data.loc[data_rows - 1, 'passer_id']==data.loc[data_rows - 2, 'passer_id']:
        game_num[data_rows - 1] = game_num[data_rows - 2] + 1
    
    # convert game_num to DataFrame
    game_num = pd.DataFrame(game_num,range(0,data_rows),['game_num'])
    
    # combine game_num into data
    data = pd.concat([data, game_num], axis=1)
    
    # find how big the chart is
    game_num_max = data.loc[:,'game_num'].max()
    
    # find who played the most games -- not used
    game_num_max_idx = data.loc[:,'game_num'].idxmax()
    who_game_num_max = data.loc[game_num_max_idx,'passer']
    
    # create cumulative epa column - use game epa as starting point
    cum_soi = data.loc[:,'qb_epa']
    
    # get ready for for loop
    k = 1
    pd.options.mode.chained_assignment = None  # default='warn'
    
    # find cumulative epa's by passer game number
    for m in data.loc[:,'passer_id']:  
        if k == data_rows - 1:
            break
        if data.loc[k + 1, 'game_num'] > 1:
            cum_soi[k + 1] = cum_soi[k + 1] + cum_soi[k]
        k = k + 1
    pd.options.mode.chained_assignment = 'warn'  # default='warn'
    
    # find the highest EPA for game 1, game 2, etc.
    data = data.sort_values(by=['game_num','qb_epa']).reset_index(drop=True)
    
    # reorder columns for easy pasting
    data = data.reindex(columns=['game_num', 'passer', 'qb_epa', 'posteam', 'game_id', 'passer_id'])
    
    # round epa
    data.loc[:,'qb_epa'] = np.round(data.loc[:,'qb_epa'],1)
    data_return = data
    
    # initialize some lists
    list_game_num = np.arange(1,game_num_max,dtype=int)
    game_num_count = np.arange(1,game_num_max,dtype=int)
    
    # find how many passers played 1 game, 2 games, 3 games, etc
    n = 1
    for n in list_game_num:
        game_num_count[n-1] = data.loc[(data.game_num==n),"passer_id"].count()
    
    # find the index for the last game 1, game 2, game 3, etc
    # this will be the index for the passer name and epa total for the final chart
    data_index = np.zeros(int(game_num_max))
    
    for p in range(0,int(game_num_max-1)):
        data_index[p] = game_num_count[p] + data_index[p-1]
    
    # fix the last one
    data_index[n] = game_num_count[p] + data_index[p-1] + 1
    
    # make the chart
    the_list = data.loc[data_index-1].reset_index(drop=True)
    the_list = the_list.rename(columns={"game_num": "Gm", "passer": "QB", "qb_epa": "EPA"})
    
    # fix Aaron Rodger's name
    the_list = the_list.replace('Aa.Rodgers','A.Rodgers')
    
    # import or calculate each passer's final game played
    gms_played = data.groupby('passer_id')['game_num'].max().reset_index()
    manning_gms = pd.DataFrame(np.array([['99-0000002', 266]]),columns=['passer_id', 'game_num'])
    gms_played = pd.concat([gms_played, manning_gms], axis=0, sort=True, ignore_index=True)
    
    # add an asterisk
    w=0
    for u in the_list.loc[:,'passer_id']:
        u_idx = gms_played.index[gms_played['passer_id'] == u].to_list()
        u_idx = u_idx[0]
        if gms_played.loc[u_idx,'passer_id'] == u and gms_played.loc[u_idx,'game_num'] == the_list.loc[w,'Gm']:
            the_list.loc[w,'QB'] = the_list.loc[w,'QB']+'*'
        # indiscriminantly give Warner and Fitzpatrick the older Rams colors
        # this will be a problem if they show up on the chart as non-Rams
        if u == '00-0017200' or u == '00-0023682':
            the_list.loc[w,'posteam'] = 'STL'
        w = w + 1
    
    # add style column
    the_list['style'] = 'normal'
    
    # check each entry to see if it should be italicized
    pd.options.mode.chained_assignment = None  # default='warn'
    for i in range(1,len(the_list.index)):
        # find the highest EPA and it's location on the chart
        max_epa = the_list['EPA'].head(i).max()
        max_index = the_list['EPA'].head(i).idxmax()
        if the_list['EPA'][i] < max_epa and the_list['passer_id'][i] != the_list['passer_id'][max_index]:
            the_list['style'][i] = 'italic'
    pd.options.mode.chained_assignment = 'warn'  # default='warn'
    
    # change floats to ints
    the_list['Gm'] = the_list['Gm'].astype(int)
    
    # save to image w/ format_table (with annoying vertical line adjustment)
    # if the vertical lines aren't lined up properly, tweak the last argument
    df2table(the_list,chart_rows,'EPA_chart.png',0.994)
    print('')
    
    # calculate and display time elapsed
    t_1 = time.time()
    elapsed_1 = t_1 - t_0
    print('Total EPA took', round(elapsed_1), 'seconds')
    
    return(data_return,the_list)

if __name__ == '__main__':
    tot_epa_data,tot_epa_list = epa_func(2022,35)
