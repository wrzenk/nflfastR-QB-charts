# Most EPA after n career games

This repository uses nflfastR play-by-play data to create charts like this:

![Most EPA after n games (updated Apr 2023)](https://i.imgur.com/yRMx3Vv.png)

Explanation of how to read this chart: It is essentially a long list of records. If you want to know which QB had the most career EPA after 50 games, find the "Gm" column with the number 50. That row will show you that Mahomes holds the record with 726.3 EPA after his 50th career game. If you want to know who holds the record for 150 career games, find the "Gm" column with 150. That row shows Aaron Rodgers holds the record with 1452.4 EPA.

An asterisk indicates a QB's last game played. An italicized entry indicates a different QB has more EPA with fewer games played. These charts include both regular season and playoff games. They do not include games where the QB had zero dropbacks.

# Usage
Run 'nflfastR_download.py' to download and filter the play-by-play data from 1999 to present. Then run 'weekly_chart_update.py' to create the charts. The nflfastR data is usually updated several hours after the completion of each game.

Developed with:
- Python 3.9.12
- pandas 1.4.2
- numpy 1.21.5
- matplotlib 3.5.1

# Acknowledgements
- The [nflfastR](https://www.nflfastr.com/) team for providing the free play-by-play data
- The open source community for helping me learn Python and publish my first project
