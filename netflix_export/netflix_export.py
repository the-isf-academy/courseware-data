import pandas as pd


def parse_df(df):
    media_type = []

    for title in netflix_df["Title"]:
        if 'Season' in title:
            media_type.append('tv')
        elif title.count(':') > 1:
            media_type.append('other')

        else:
            media_type.append('movie')
    
    df['media_type'] = media_type
    return df

if __name__ == '__main__':

    netflix_df = pd.read_csv('data/NetflixViewingHistory.csv')
    
    netflix_df_updated = parse_df(netflix_df)
    


    netflix_df_updated.to_csv (r'export/watch-history-full.csv', index = None)

    print("----- Finished Export -----")
