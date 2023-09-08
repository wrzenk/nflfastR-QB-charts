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

nfl_year = 2023  # ongoing season to update (re-download & process)

# start timer
t_0=time.time()

# download data if hrs hours has elapsed from last download
print(f'downloading {nfl_year} data')
nflfastR_download.download_years(nfl_year,nfl_year)

# update epa chart
tot_epa_data = epa_func(nfl_year,35) # 2nd arg defines rows in final chart

# update epa/dropback
epapp_data = epa_dpbk(nfl_year,35) # 2nd arg defines rows in final chart

# calculate and display time elapsed
t_f = time.time()
elapsed_1 = round(t_f - t_0)
elapsed_min = elapsed_1/60
print(f'all updates took {elapsed_1} seconds or {elapsed_min:0.2f} mins')
