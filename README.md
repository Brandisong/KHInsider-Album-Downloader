# KHInsider-Album-Downloader
A python script which is passed the url for an album from https://downloads.khinsider.com/, which scrapes and downloads all tracks in .mp3 or .flac format.

Written using Python 3. Uses the path module, so is appropriate for Windows and Unix-based operating systems.

I hope this script saves you a lot of time. It is lightweight and simple compared to others, I mostly wrote it as an exercise in webscraping.
<h2>Prerequisites</h2>
This script uses <i>requests, beautifulsoup 4,</i> and <i>pathlib</i> third party modules.
If you don't have them, you must use 'pip install [requests / beautifulsoup4 / pathlib' for the script to run.

You also need Python 3 to run the script. Both Python and pip can be installed from [here.](https://www.python.org/downloads/)
<h2>Usage</h2>
Run from commandline:

> py khi_scraper [url] [--mp3 / --flac]

E.g. to download the King's Field 4 OST in .mp3 format:

> py khi_scraper https://downloads.khinsider.com/game-soundtracks/album/king-s-field-iv-the-ancient-city-gamerip --mp3

Alternatively, if you wanted .flac files, substitute --mp3 with --flac.

<h2>Output</h2>
This will create a folder of the album name <b>in the current working directory,</b> and download each of the listed tracks with appropriate order and title names. MP3 files come with appropriate metadata, and tracks are named with a numbered prefix.
