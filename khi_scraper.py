# Written by Brandisong 24/05/2024

import sys, requests, re, bs4
from pathlib import Path

# Check if an argument was passed
if len(sys.argv) < 3:
    print("Usage: khi_scraper [url] [--mp3 / --flac]")
    sys.exit()
else:
    url = sys.argv[1]
    fileType = sys.argv[2][2:] # sets to mp3 or flac according to arg

    # Check if khi link is valid
    if "https://downloads.khinsider.com/game-soundtracks/" not in url:
        print("Invalid url, please use https://downloads.khinsider.com/game-soundtracks/")
        sys.exit()

    # Check if filetype arg is correct
    if (fileType != "mp3") and (fileType != "flac"):
        print(fileType)
        print("Usage: khi_scraper [url] [--mp3 / --flac]")
        sys.exit()

# Attempt to get the web page
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
res = requests.get(url, headers=headers)

# Check to see if it worked
if res.status_code != requests.codes.ok:
    print("Request failed, please check the link and try again.")
    print("Returned with code " + str(res.status_code))
    sys.exit()

# Parse with bs4
khiSoup = bs4.BeautifulSoup(res.text, features="html.parser")

# Check if empty
emptyCheck = khiSoup.select('#pageContent > h2')
if str(emptyCheck) == "[<h2>Ooops!</h2>]":
    print("Error: KHI doesn't have that link")
    sys.exit()
del emptyCheck
print("Request successful")

# Select all links ending in .mp3
links_blob = khiSoup.select('tr > td.clickable-row > a[href$=".mp3"]')

# Extract all links in the object using regex
khiRegex = re.compile(r'/game-soundtracks/(.)+.mp3')
# Create a list of all matched links
link_list = []
for x in range(len(links_blob)):
    link_list.append(khiRegex.search(str(links_blob[x])))

# Create list of link strings
clean_list = []
for x in link_list:
    if ("https://downloads.khinsider.com/" + x.group()) not in clean_list:
        clean_list.append("https://downloads.khinsider.com/" + x.group())

# Print each link
# for x in clean_list:
#     print(x)
totalTracks = len(clean_list)
print(str(totalTracks) + " tracks found")
trackCount = 1

# Get the album name
albumName = khiSoup.select("#pageContent > h2")[0]
albumName = str(albumName)[4:len(albumName)-6]
print(albumName)
albumNameAlNum = ''.join(x for x in albumName if x.isalnum())

# Make album directory in downloads, else in working directory
if Path(Path.home(), "Downloads").exists:
    Path(Path.home(), "Downloads", albumNameAlNum).mkdir()
else:
    Path(albumNameAlNum).mkdir()

# Get each song download link from the unique list
for url in clean_list:
    res = requests.get(url, headers=headers)
    res.raise_for_status() # Exit if it fucked up

    # Parse with bs4
    khiSoup = bs4.BeautifulSoup(res.text, features="html.parser")

    # Get mp3 selector
    if fileType == "mp3":
        selectCSS = "#pageContent > p:nth-child(9) > a"
    # Get flac selector
    elif fileType == "flac":
        selectCSS = "#pageContent > p:nth-child(10) > a"
    else:
        print("Error: invalid file type")
        sys.exit()
    
    # Get the title of the track
    trackName = khiSoup.select("#pageContent > p:nth-child(6) > b:nth-child(3)")[0]
    trackName = str(trackName)[3:len(trackName)-5]

    # Print info to terminal
    print(f"{str(trackCount)} / {str(totalTracks)}: {str(trackName)}")
    downloadLink = khiSoup.select(selectCSS)[0]

    # Download the song
    res = requests.get(downloadLink.get('href'))

    # Change directory to working directory if there's no Downloads folder
    if Path(Path.home(), "Downloads").exists:
        directory = Path(Path.home(), "Downloads", albumNameAlNum, (str(trackCount) + " " + trackName + "." + fileType))
    else:
        directory = Path(albumNameAlNum, (str(trackCount) + " " + trackName + "." + fileType))
    
    trackFile = open(directory, 'wb')
    for chunk in res.iter_content(100000):
        trackFile.write(chunk)
    trackFile.close()

    trackCount += 1

print("All files successfuly downloaded")