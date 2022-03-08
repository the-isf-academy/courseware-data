# Spotify Export

This script converts the Spotify `StreamingHistory0.json` into a csv file. It also uses the [Spotify Web API](https://developer.spotify.com/documentation/web-api/reference/#/) to populate the csv with track and artist specific statistics.

## Installation

First, install the packages these scripts require:

`pip3 install  -r requirements.txt`

## Add personalized Spotify json to repo

First, you will need to request and download your Spotify [account data](https://www.spotify.com/us/account/privacy/). This may take up to 30 days (but will probably be closer to 3 days).

Once you receive the email confirming your data is ready to download, download the `.zip` files. Then, upzip the files in your `/downloads` folder.

Go into the `MyData` folder to find the `StreamingHistory0.json` file.

Then, copy+paste or drag+drop the `StreamingHistory0.json` file into the `/data` folder of this repository.

## Get Your Client ID and Client Secret

Second, you need to create an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and copy the Client ID and Client Secret.  Reference [this video](https://youtu.be/or6GSvjmyyE) for a demonstration.

Once you've completed this step, paste the Client ID into the `data/client_id.txt` file, and paste the Client Secret into the `data/client_secret.txt` file.

## Add your Redirect URI

Third, you need to add your URI. On that same [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) click Edit Settings and paste in http://127.0.0.1:9090 as your Redirect URI.  Reference [this video](https://youtu.be/B_NYjslAGfw) for a demonstration.

## Running the script

Run this script using the following command:

`python3 spotify_export.py`

The script will take a long time to execute. When it is finished, you can find your data in the `exports/` directory.
