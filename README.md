# Most EPA after n career games: nflfastR QB charts

![Most EPA after n games (updated Apr 2023)](https://i.imgur.com/yRMx3Vv.png)

Explanation of how to read this chart. It is essentially a long list of records. If you want to know which QB had the most career EPA after 50 games, find the "Gm" column with the number 50. That row will show you that Mahomes held the record with 726.3 EPA after his 50th career game. An asterisk indicates a QB's last game played. Italics indicate a QB has more EPA with fewer games played.

These charts include both regular season and playoff games. They do not include games where the QB had zero dropbacks. Aaron Rodgers had one such game January 1, 2006 when he had one kneel down.

# Usage
Run 'nflfastR_download.py' to download and filter the play-by-play data from 1999 to present. Then run 'weekly_chart_update.py' to create the charts. The nflfastR data is usually updated several hours after the completion of each game.

Developed with:
- Python 3.9.12
- pandas 1.4.2
- numpy 1.21.5
- matplotlib 3.5.1

# Big thanks to:
- The [nflfastR](https://www.nflfastr.com/) team for providing the free play-by-play data
- The open source community for helping me learn Python and publish my first project
