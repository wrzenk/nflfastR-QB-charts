"""
This file reads in csv files from nflfastR's dataset (1999-current). Then finds which passer has the most qb_epa per dropback after n games, for n = 1 up to the most games played. It exports a csv and a .png file. It returns the filtered data in a dataframe.

I annoyingly use "per play" and "per dropback" interchangeably throughout this script

"""

import time
import sys
import pandas as pd
import numpy as np
from format_table import df2table

def epa_dpbk(last_year,chart_rows=35):
    # start timer
    t_0=time.time()
    
    #######################################################################
    # specify first year to process
    first_year = 1999
    # minimum dropbacks per game (cumulative)
    min_dropbacks = 10
    #######################################################################
    
    # initialize some stuff
    years = list(range(first_year,last_year + 1))
    filt_data = pd.DataFrame()
    data = pd.DataFrame()
    
    # read raw data and filter it
    for i in years:  
        sys.stdout.write("\r")
        sys.stdout.write("processing EPA/play for {:2d}".format(i))
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
                                          'qb_dropback'
                                          ]].sum().reset_index()
        # combine into one file
        # data = data.append(filt_data, sort=True) # deprecated
        data = pd.concat([data,filt_data])
    
    # drop Brad Johnson because he just doesn't belong there...sorry dude
    data = data[data["passer"].str.contains("B.Johnson")==False]
    
    # sort by game_id, then by passer
    data = data.sort_values(by=['passer_id','game_id']).reset_index(drop=True)
    
    # get a list of all passer names -- not used yet
    passer_list = data.loc[:,'passer']
    passer_list = passer_list.drop_duplicates()
    
    # find how many player-games there are
    data_rows = len(data)
    
    # inialize some stuff
    game_num = np.ones(data_rows)
    j = 0
    
    # create game number data
    for w in data.loc[:,'passer_id']:  
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
    
    # get ready for for loop
    q = 0
    # create cumulative qb_dropback column - use qb_dropback as starting point
    cum_qb_dropback = data.loc[:,'qb_dropback']
    
    # eliminate annoying warning for a bit
    pd.options.mode.chained_assignment = None
    
    # find cumulative qb_dropback's by passer game number
    for r in data.loc[:,'passer_id']:  
        if q == data_rows - 2:
            break
        if data.loc[q + 1, 'game_num'] > 1:
            cum_qb_dropback[q + 1] = cum_qb_dropback[q] + cum_qb_dropback[q + 1]
        q = q + 1
    # fix the last row
    if data.loc[data_rows - 1, 'passer_id']==data.loc[data_rows - 2, 'passer_id']:
        cum_qb_dropback[data_rows - 1] = cum_qb_dropback[data_rows - 2] + cum_qb_dropback[data_rows - 1]
    
    # get a list of all passer names -- not used yet
    passer_list = data.loc[:,'passer']
    passer_list = passer_list.drop_duplicates()
    
    # find how big the chart is
    game_num_max = data.loc[:,'game_num'].max()
    
    # find who played the most games -- not used
    game_num_max_idx = data.loc[:,'game_num'].idxmax()
    who_game_num_max = data.loc[game_num_max_idx,'passer']
    
    # create cumulative epa column - use game epa as starting point
    cum_epa = data.loc[:,'qb_epa']
    
    # get ready for for loop
    k = 0
    
    # find cumulative epa's by passer game number
    for m in data.loc[:, 'passer_id']:  
        if k == data_rows - 2:
            break
        if data.loc[k + 1, 'game_num'] > 1:
            cum_epa[k + 1] = cum_epa[k + 1] + cum_epa[k]
        k = k + 1
    
    #fix last row...
    if data.loc[data_rows - 1, 'passer_id']==data.loc[data_rows - 2, 'passer_id']:
        cum_epa[data_rows - 1] = cum_epa[data_rows - 2] + cum_epa[data_rows - 1]
    
    # stop suppressing annoying warning
    pd.options.mode.chained_assignment = 'warn'
    
    # calculate cumulative epa per play for each passer
    epapp = data.loc[:,'qb_epa'] / data.loc[:,'qb_dropback']
    epapp = pd.DataFrame(epapp,columns=['epapp'])
    
    # combine epapp into data
    data = pd.concat([data, epapp], axis=1)
    
    # find rows to be dropped - at least 10 dropbacks per game (cumulative)
    to_drop = data.index[data['qb_dropback'] < min_dropbacks * data['game_num']]
    
    # drop them
    data = data.drop(to_drop)
    
    # find the highest EPA for game 1, game 2, etc.
        # sort by epa within each game_num
    data = data.sort_values(by=['game_num','epapp']).reset_index(drop=True)
    
    # reorder columns for easy pasting
    data = data.reindex(columns=['game_num', 'passer', 'epapp', 'posteam', 'game_id', 'passer_id', 'qb_dropback', 'qb_epa'])
    
    # round epapp
    data.loc[:,'epapp'] = np.round(data.loc[:,'epapp'], 3)
    epapp_return_data = data
    
    # initialize some lists
    list_game_num = np.arange(1,game_num_max,dtype=int)
    game_num_count = np.arange(1,game_num_max,dtype=int)
    
    # find how many passers played 1 game, 2 games, 3 games, etc
    n = 1
    for n in list_game_num:
        game_num_count[n-1] = data.loc[(data.game_num==n), 'passer_id'].count()
    
    # find the index for the highest game 1, game 2, game 3, etc
    # this "should" be the index for the passer name and epa total for the final chart
    data_index = np.zeros(int(game_num_max))
    
    for p in range(0,int(game_num_max-1)):
        data_index[p] = game_num_count[p] + data_index[p-1]
    
    # fix the last one
    data_index[n] = game_num_count[p] + data_index[p-1] + 1
    
    # make the chart
    the_EPA_per_play_chart = data.loc[data_index-1].reset_index()
    
    # fix Aaron Rodger's name
    the_EPA_per_play_chart = the_EPA_per_play_chart.replace('Aa.Rodgers','A.Rodgers')
    
    # import or calculate each passer's final game played
    gms_played = data.groupby('passer_id')['game_num'].max().reset_index()
    
    # add an asterisk
    w=0
    for u in the_EPA_per_play_chart.loc[:,'passer_id']:
        u_idx = gms_played.index[gms_played['passer_id'] == u].to_list()
        u_idx = u_idx[0]
        if gms_played.loc[u_idx,'passer_id'] == u and gms_played.loc[u_idx,'game_num'] == the_EPA_per_play_chart.loc[w,'game_num']:
            the_EPA_per_play_chart.loc[w,'passer'] = the_EPA_per_play_chart.loc[w,'passer']+'*'
        # give Warner the right colors
        if u == '00-0017200':
            the_EPA_per_play_chart.loc[w,'posteam'] = 'STL'
        w = w + 1
    
    # reorder columns for easy pasting
    the_EPA_per_play_chart = the_EPA_per_play_chart.reindex(columns=['game_num', 'passer', 'epapp', 'posteam', 'game_id', 'passer_id', 'qb_dropback', 'qb_epa','index'])
    
    # rename columns
    the_EPA_per_play_chart = the_EPA_per_play_chart.rename(columns={"game_num": "Gm", "passer": "QB", "epapp": "EPA/p"})
    
    # deal with decimals
    the_EPA_per_play_chart['Gm'] = the_EPA_per_play_chart['Gm'].astype(int)
    the_EPA_per_play_chart.update(the_EPA_per_play_chart[['EPA/p']].applymap('{:,.3f}'.format))
    
    # add style column (not used for rate stats)
    the_EPA_per_play_chart['style'] = 'normal'
    
    # save chart as image (with annoying vertical line adjustment)
    df2table(the_EPA_per_play_chart,chart_rows,'EPApp_chart.png',0.996)
    
    # save the chart as csv (not needed anymore since I created df2table)
    # the_EPA_per_play_chart.to_csv('the_EPA_per_play_chart_' + str(first_year) + '_to_' + str(last_year) + '.csv', compression=None, index=False)
    
    t_1 = time.time()
    elapsed_1 = t_1 - t_0
    print('')
    print('EPA/play took', round(elapsed_1), 'seconds')
    return(epapp_return_data)

if __name__ == '__main__':
    epa_dpbk(2022,35)
