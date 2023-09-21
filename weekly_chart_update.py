"""
Run nflfastR_download.py first to download data from 1999 to present. Then use this script to create charts and keep them updated weekly.

This script uses the following scripts:
    nflfastR_download.py
    most_qb_epa_after_n_games.py
        format_table.py
    most_EPApplay_after_n_games.py
        format_table.py

"""
import time
import nflfastR_download
from most_EPApplay_after_n_games import epa_dpbk
from most_qb_epa_after_n_games import epa_func

nfl_year = 2023  # change this once every year, after week 1
chart_rows = 35  # number of rows to put in charts (use 383 for 1 column)

# start timer
t0=time.time()

# download data to update this year's data
print(f'downloading {nfl_year} data')
nflfastR_download.download_years(nfl_year,nfl_year)

# update epa chart
tot_epa_data = epa_func(nfl_year,chart_rows)

# update epa/dropback
epapp_data = epa_dpbk(nfl_year,chart_rows)

# calculate and display time elapsed
elapsed = time.time() - t0
elapsed_min = elapsed/60
print(f'all updates took {elapsed:,.1f} seconds or {elapsed_min:,.2f} mins')
