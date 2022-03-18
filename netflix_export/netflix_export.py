import pandas as pd


def parse_df(df):
    media_type = []
    title_list = []
    season = []
    episode = []


    for title in netflix_df["Title"]:
        if 'Season' in title:
            media_type.append('tv')

            title_split = title.split(":")

            title_list.append(title_split[0])
            season.append(title_split[1])
            episode.append(title_split[2])

        elif title.count(':') > 1:
            media_type.append('other')
            title_list.append(None)
            season.append(None)
            episode.append(None)

        else:
            media_type.append('movie')
            title_list.append(None)
            season.append(None)
            episode.append(None)
    
    df['media_type'] = media_type
    df['tv_show_title'] = title_list
    df['season'] = season
    df['episode'] = episode
    return df

if __name__ == '__main__':

    netflix_df = pd.read_csv('data/NetflixViewingHistory.csv')
    
    netflix_df_updated = parse_df(netflix_df)
    


    netflix_df_updated.to_csv (r'export/watch-history-full.csv', index = None)

    print("----- Finished Export -----")
