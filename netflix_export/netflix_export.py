import pandas as pd


def parse_df(df):
    media_type = []
    title_list = []
    season = []
    episode = []


    for title in netflix_df["Title"]:
        if 'Season' in title:
            media_type.append('series')

            title_split = title.split(":")
            if any(char.isdigit() for char in title_split[1]):
                series_season_list = title_split[1].split(' ')

            title_list.append(title_split[0])
            season.append(series_season_list[-1])
            episode.append(title_split[2])

        elif title.count(':') == 1:
            # print(title)
            title_split = title.split(": ")
            # print(title_split)
            media_type.append('series')

            title_list.append(title_split[0])
            season.append(None)
            episode.append(title_split[1])


        elif title.count(':') > 1:
            title_split = title.split(": ")
            # print(title_split)
            if any(char.isdigit() for char in title_split[1]):
                series_season_list = title_split[1].split(' ')

                print(title_split[1],series_season_list)

            media_type.append('series')

            title_list.append(title_split[0])
            season.append(series_season_list[-1])
            episode.append(None)

        elif ':' in title:

            media_type.append('series')

            title_split = title.split(": ")
            # print(title, title_split)

            title_list.append(title_split[0])
            season.append(title_split[1])
            # episode.append(title_split[])


        else:
            media_type.append('movie')
            title_list.append(None)
            season.append(None)
            episode.append(None)
    
    df['media_type'] = media_type
    df['series_title'] = title_list
    df['season'] = season
    df['episode'] = episode
    return df

if __name__ == '__main__':

    netflix_df = pd.read_csv('data/NetflixViewingHistory.csv')
    
    netflix_df_updated = parse_df(netflix_df)
    


    netflix_df_updated.to_csv (r'export/watch-history-full.csv', index = None)

    print("----- Finished Export -----")
