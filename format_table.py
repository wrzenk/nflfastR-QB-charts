"""
This script accepts a dataframe with the following columns: 
    games, qb, stat, team, style.

The first 3 columns go on the chart. Team column determines the color of the 
cell and text (per the tm_color_lkup dictionary defined below). The style 
column specifies if the entry should be italicized or normal.

The factor variable is a really annoying thing. When I get the coordinates for 
the placement of the black vertical lines, they are scaled outward from the 
middle by just a little--usually just a few pixels at the edge. The factor 
squishes them back toward the middle. A factor value of 1 will not have any 
effect on the line placement. The factor usually needs to be smaller as more 
columns are added to the chart. I haven't figured out an easy way to calculate 
the needed adjustment, so for now it is hard coded for each chart and passed 
into this script. Very annoying.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats

def df2table(data,want_rows = 3,filename = 'tableplot.png',factor = 0.995):
    # define team colors in a dict 
    # 'Team abbreviation':['background color','font color']
    tm_color_lkup = {'KC' :['#FF0000','#FFFF00'],
                     'GB' :['#38761d','#FFFF00'],
                     'ARI':['red','#FFFFFF'],
                     'ATL':['dimgray','red'],
                     'BAL':['#8300da','purple'],
                     'BUF':['#00338D','red'],
                     'CAR':['#181818','#36d2f8'],
                     'CHI':['#ed8114','#000292'],
                     'CIN':['#FB4F14','black'],
                     'CLE':['#a0683c','brown'],
                     'DAL':['silver','darkblue'],
                     'DEN':['#ff8c12','#002244'],
                     'DET':['#d9d9d9','#2d6596'],
                     'HOU':['#003362','#ff0000'],
                     'IND':['white','#073763'],
                     'JAX':['#2fcec0','black'],
                     'JAC':['#2fcec0','black'],
                     'LAC':['#6d9eeb','yellow'],
                     'SD' :['#6d9eeb','yellow'],
                     'SDG':['#6d9eeb','yellow'],
                     'LAR':['blue','yellow'],
                     'LA' :['blue','yellow'],
                     'STL':['#073763','#f9cb9c'],
                     'MIA':['#3aa3d8','white'],
                     'MIN':['#46259c','yellow'],
                     'NE' :['#1c4587','#d9d9d9'],
                     'NO' :['#bf9000','black'],
                     'NYG':['mediumblue','white'],
                     'NYJ':['#1a8562','white'],
                     'OAK':['#181818','silver'],
                     'LV' :['#181818','silver'],
                     'LVR':['#181818','silver'],
                     'PHI':['#408322','silver'],
                     'PIT':['yellow','black'],
                     'SEA':['#0B5394','chartreuse'],
                     'SF' :['#AA0000','gold'],
                     'TB' :['#474641','#ff3535'],
                     'TEN':['#073763','lightsteelblue'],
                     'WAS':['#990000','#f9cb9c']
                    }
    
    # parse dataframe into useful pieces
    df = data.iloc[: , :3]
    tm = data['posteam']
    chrt_styles = data['style']
    
    # initialize color lookup table
    chrt_colors = []
    
    # fill in color lookup table by using team color dict
    for j in tm:
        chrt_colors.append(tm_color_lkup[j])
    
    # create and format figure
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    font = 'Calibri'
    weight = 'bold'
    
    plt.rcParams['font.family'] = font
    
    # find dimensions of dataframe
    num_rows = len(df)
    entries = num_rows
    num_cols = len(df.columns)
    col_names = list(df.columns)
    empty_list = [''] * num_cols
    
    # find number of blank rows to add to make multiple of want_rows
    num_to_add = want_rows - (num_rows % want_rows)
    df_to_add = pd.DataFrame(np.array([empty_list]), columns = col_names)
    for x in range(num_to_add):
        df = pd.concat([df,df_to_add], ignore_index = True)
        chrt_colors.append('w')
    
    # find new dimenstions of dataframe
    col_repeats = int(np.ceil(num_rows / want_rows))
    col_names = col_names * col_repeats
    want_cols = col_repeats * num_cols
    
    # duplicate the columns across
    wide_df = pd.DataFrame(df, columns = col_names)
    
    # shift the data up in the repeated columns
    mcell_row = 0 # row of cell to be moved
    mcell_col = 0 # col of cell to be moved
    dcell_row = 0 # destination row of cell to be moved
    dcell_col = 0 # destination col of cell to be moved
    for f in range(1,col_repeats):
        for e in range(0,want_rows):
            for d in range(0,num_cols):
                mcell_row = e + (want_rows * f)
                mcell_col = d + (num_cols * f)
                dcell_row = mcell_row - (want_rows * f)
                dcell_col = mcell_col
                wide_df.iloc[dcell_row,
                             dcell_col] = wide_df.iloc[mcell_row,
                                                       mcell_col]
    
    # delete the unneeded rows
    wide_df = wide_df.truncate(after=want_rows - 1)
    
    # adjust to the new dimensions
    num_rows = len(wide_df)
    num_cols = len(wide_df.columns)
    
    # create default colors for dataframe
    cell_colors = [['w'] * num_cols]
    i = 0
    while i < num_rows - 1:
        cell_colors.append(['w'] * num_cols)
        i = i + 1
    
    # fill in cell colors
    entry_ctr = 0
    col_ctr = 0
    for j in range(0,int(num_cols/3)):
        for i in range(0,want_rows):
            cell_colors[i][0 + col_ctr * 3] = chrt_colors[entry_ctr][0]
            cell_colors[i][1 + col_ctr * 3] = chrt_colors[entry_ctr][0]
            cell_colors[i][2 + col_ctr * 3] = chrt_colors[entry_ctr][0]
            entry_ctr += 1
        col_ctr += 1
    
    # create the table
    table = ax.table(cellText = wide_df.values,
                     colLabels = wide_df.columns,
                     loc = 'center',
                     cellColours = cell_colors,
                     cellLoc = 'left'
                     )
    # set header color
    for cel in range(want_cols):
        table[(0,0+cel)].set_facecolor('#dddddd')
        table[(0,0+cel)].get_text().set_color('#333333')
    # format the table
    table.auto_set_column_width(col=list(range(len(wide_df.columns))))
    table.set_fontsize(10)
    y_cell_scale = 1.05
    table.scale(1,y_cell_scale)
    
    # make all text bold
    for i in range(num_rows + 1):
        for j in range(num_cols):
            table[(i,j)].get_text().set_weight(weight)
    
    # set the text color and style
    entry_ctr = 0
    col_ctr = 0
    for j in range(0,int(num_cols/3)):
        for i in range(1,want_rows+1):
            if entry_ctr >= entries:
                break
            table[(i, 0 + col_ctr * 3)].get_text().set_color(chrt_colors[entry_ctr][1])
            table[(i, 1 + col_ctr * 3)].get_text().set_color(chrt_colors[entry_ctr][1])
            table[(i, 2 + col_ctr * 3)].get_text().set_color(chrt_colors[entry_ctr][1])
            table[(i, 0 + col_ctr * 3)].set_text_props(style = chrt_styles[entry_ctr])
            table[(i, 1 + col_ctr * 3)].set_text_props(style = chrt_styles[entry_ctr])
            table[(i, 2 + col_ctr * 3)].set_text_props(style = chrt_styles[entry_ctr])
            entry_ctr += 1
        col_ctr += 1
    
    # change padding from 10% to 5% for QB columns (is this necessary???)
    qb_cols = np.arange(1,45,3)
    for key,cell in table.get_celld().items():
        for m in qb_cols:
            if key[1]==m:
                cell.PAD = 0.05
    
    # get the cell dimensions
    cells = table.get_celld()
    loc = []
    plt.draw()
    for p in range(0,want_rows+1):
        for q in range(want_cols):
                cells[(p,q)].set_edgecolor('whitesmoke')
                loc.append(cells[(p,q)].xy)
    
    # update plot to get accurate cell sizes
    plt.draw()
    
    # get the cell height. Should be the same for every cell
    height = loc[0][1] - loc[want_cols][1]
    
    yloc = np.zeros(want_rows + 2)
    yloc[0] = loc[0][1]+height
    for y in range(1,want_rows+2):
        yloc[y] = yloc[y-1]-height
    
    # get the widths of each column
    # why is this not accurate???
    xloc = np.zeros(want_cols + 1)
    for w in range(want_cols):
        xloc[w] = loc[w][0]
    last_col_wid = cells[(want_rows,want_cols-1)].get_width()
    xloc[w+1] = xloc[w] + last_col_wid
    
    # correct the x values toward the middle by a "squish" factor
    # the x coordinates are almost always too wide
    xmean = stats.mean(xloc)
    for num in range(len(xloc)):
        xloc[num] = xmean + factor * (xloc[num] - xmean)
    
    # draw horizontal line across the whole table
    def horiz(row,want_cols):
        plt.annotate(None,                          # arrow head style
                    (xloc[0],yloc[row]),            # starting point of line
                    (xloc[want_cols],yloc[row]),    # end point of line
                    xycoords = 'axes fraction',
                    arrowprops = {'arrowstyle':'-',
                                  'color':'#333333',
                                  'lw':'1.5'
                                  })
    
    # draw vertical line through the table
    def vert(col,want_rows):
        plt.annotate(None,
                    (xloc[col],yloc[0]),
                    (xloc[col],yloc[want_rows]),
                    xycoords = 'axes fraction',
                    arrowprops = {'arrowstyle':'-',
                                  'color':'#333333',
                                  'lw':'1.5'
                                  })
    
    # header lines
    horiz(0,want_cols)
    horiz(1,want_cols)
    
    # bottom line
    horiz(want_rows+1,want_cols)
    
    # draw a vertical line every 3 columns
    for lin in range(want_cols+1):
        if lin%3 == 0:
            vert(lin,want_rows+1)
    
    # save and show the table
    # fig.canvas.draw() # I don't know where this line came from or what it does
    plt.draw()
    plt.savefig(filename, bbox_inches="tight", dpi = 120)
    plt.show()
    return

if __name__ == '__main__':
    # create fake data for testing
    df = pd.DataFrame(np.array([[1,'K.Warner',12,'STL','normal'],
                                [2,'D.Brees',10,'NO','italic'],
                                [3,'D.Brees',13,'NO','normal'],
                                [4,'P.Mahomes',12,'KC','italic'],
                                [5,'P.Mahomes',18,'KC','normal'],
                                [6,'P.Mahomes',22,'KC','normal'],
                                [7,'P.Mahomes',28,'KC','normal'],
                                [8,'P.Mahomes',32,'KC','normal'],
                                [9,'P.Mahomes',47,'KC','normal']
                               ]
                               ),
                              columns = ['Gm','QB','TDs','posteam','style'])
    df2table(df,7,'tabletest.png',1.000)
