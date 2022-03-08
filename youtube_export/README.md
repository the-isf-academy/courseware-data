# Youtube Export 

This script converts the Youtube `watch-history.json` into a csv file. It also uses the [Youtube Data API](https://developers.google.com/youtube/v3) to populate the csv with channel and video specific statistics. 

## Installation 

First, install the packages these scripts require:

`pip3 install  -r requirements.txt`

## Add personalized Youtube json to repo

First, you will need to export your Youtube data using [Google Takeout](https://takeout.google.com/settings/takeout). This may take a couple of hours. 

Once you receive the email confirming your data is ready to download, download the `.zip` files. Then, upzip the files in your `/downloads` folder. 

Open each `Takeout` folder and find the `watch-history.json` file. It should be in one of the `/YouTube and YouTube Music` > `/history` folders

Then, move the `watch-history.json` file into the `/data` folder of this repository.

## Get API Key

Second, you need to register with Google Cloud Platform and get an API key.  

Once you have your api key, paste it into the `data/api_key.txt` file. 

## Running the script

Run this script using the following command: **`python3 youtube_export.py`**


You must go through the options in order:

0. Select `json to csv`.
1. Select `channel stats`.
2. Select `video stats`.

You can find your data in the `watch-history-full.csv` file in the `exports/` directory.

