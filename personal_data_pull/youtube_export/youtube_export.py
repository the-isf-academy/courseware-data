import pandas as pd
import json
import requests
from apiclient.discovery import build
from simple_term_menu import TerminalMenu
from tqdm import tqdm

def parse_json(file_loc):
    with open(file_loc) as json_file:
        json_list = json.load(json_file)

    json_dict = {'video_title':[],'video_id':[],'channel_name':[],'channel_id':[],'watch_date':[],'watch_time':[]}

    pbar = tqdm(total= len(json_list))

    for video in json_list:
        if 'titleUrl' in video and 'subtitles' in video:
            for key,val in video.items():
                if key=='time':
                    time_split = val.replace('Z','').split('T')
                    json_dict['watch_date'].append(time_split[0])
                    json_dict['watch_time'].append(time_split[1][:-4])
                    
                elif key == 'title':
                    json_dict['video_title'].append(val)

                elif key == 'subtitles' and val[0]['url'] != None:
                    json_dict['channel_name'].append(val[0]['name'])

                    url = val[0]['url']
                    channel_id = url.replace('https://www.youtube.com/channel/','')
                    json_dict['channel_id'].append(channel_id)

                elif key == 'titleUrl':
                    video_id = val.replace('https://www.youtube.com/watch?v=','')
                    json_dict['video_id'].append(video_id)
        pbar.update(1)

    return json_dict

def yt_api_channel(youtube, yt_df):
    pbar = tqdm(total= len(yt_df.index))

    channel_dict = {}

    json_dict = {
        'channel_view_total':[],
        'channel_subscriber_total':[],
        'channel_video_total' : []
    }

    for channel_id in yt_df['channel_id']:
        if channel_id in channel_dict:
            json_dict['channel_view_total'].append(channel_dict[channel_id]['channel_view_total'])
            json_dict['channel_subscriber_total'].append(channel_dict[channel_id]['channel_subscriber_total'])
            json_dict['channel_video_total'].append(channel_dict[channel_id]['channel_video_total'])
            # print(channel_dict)

        else:

            request = youtube.channels().list(part=['statistics'],id=channel_id)
            response = request.execute()
            if 'items' not in response:
                for column in json_dict.keys():
                    json_dict[column].append(None)

            else:
                if response['items'][0]['statistics']['hiddenSubscriberCount'] == True:
                    json_dict['channel_subscriber_total'].append(None)
                    channel_dict[channel_id] = {'channel_subscriber_total':None}
                else:
                    json_dict['channel_subscriber_total'].append(response['items'][0]['statistics']['subscriberCount'])
                    channel_dict[channel_id] = {'channel_subscriber_total':response['items'][0]['statistics']['subscriberCount']}

                json_dict['channel_view_total'].append(response['items'][0]['statistics']['viewCount'])
                json_dict['channel_video_total'].append(response['items'][0]['statistics']['videoCount'])

                channel_dict[channel_id]['channel_view_total'] = response['items'][0]['statistics']['viewCount']
                channel_dict[channel_id]['channel_video_total'] = response['items'][0]['statistics']['videoCount']
        pbar.update(1)

    pbar.close()
    return json_dict

def yt_api_video(youtube,df):
    pbar = tqdm(total= len(yt_df.index))

    video_dict = {}

    stats_columns = {
        'viewCount': 'video_view_total',
        'commentCount': 'video_comment_total',
        'likeCount': 'video_like_total',
    }


    json_dict = {
        'video_view_total': [],
        'video_like_total' : [],
        'video_comment_total' : [],
        'video_topics': []
        }

    
    for video_id in df['video_id']:

        if video_id in video_dict:
            for column in json_dict.keys():
                json_dict[column].append(video_dict[video_id][column])

        else:
            video_dict[video_id] = {}

            try:
                request = youtube.videos().list(part=['statistics','topicDetails'],id=video_id)
                response = request.execute()

                if len(response['items']) == 0:
                    for column in columns:
                        json_dict[column].append(None)

                else:

                    for column in stats_columns.keys():
                        # print(column)
                        # print(response['items'][0]['statistics'])
                        if column not in response['items'][0]['statistics']:
                            json_dict[stats_columns[column]].append(None)
                            video_dict[video_id][stats_columns[column]] = None

                        else:
                            json_dict[stats_columns[column]].append(response['items'][0]['statistics'][column])
                            video_dict[video_id][stats_columns[column]] = response['items'][0]['statistics'][column]

                    

                    if 'topicDetails' not in response['items'][0]:
                        video_topic_parsed = None
                    else:
                        video_topic = response['items'][0]['topicDetails']['topicCategories'][0]
                        video_topic_parsed = video_topic.replace('https://en.wikipedia.org/wiki/','')

                    json_dict['video_topics'].append(video_topic_parsed)
                    video_dict[video_id]['video_topics'] = video_topic_parsed

            except:
                for column in json_dict.keys():
                    json_dict[column].append(None)
                    video_dict[video_id][column] = None

        pbar.update(1)
            

    pbar.close()
    return(json_dict)

def menu():
    options = ["json to csv", "channel stats", "video stats","quit"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    option = options[menu_entry_index]

    return option

if __name__ == '__main__':

    api_key_file = open("data/api_key.txt","r")
    api_key = api_key_file.readline().replace(" ","")

    youtube = build('youtube','v3',developerKey = api_key)

    print ("-"*25)
    print("----- YOUTUBE DATA ----- ")
    print ("-"*25)

    option = menu()

    while option != "quit":
        if option == "json to csv":
            json_dict = parse_json('data/watch-history.json')
            json_to_csv_df = pd.DataFrame.from_dict(json_dict)
            json_to_csv_df.to_csv(r'export/json-parsed.csv',index=None)

        elif option == 'channel stats':
            original_csv_df = pd.read_csv('export/json-parsed.csv')

            unique_channels = original_csv_df['channel_id'].nunique()

            if unique_channels > 10000:
                print("Due to API quota, your dataset is too large.")
                rows_dropped = 0
                pbar = tqdm(total= abs(unique_channels-10000))
                drop_rows = unique_channels - 10000

                while unique_channels > 10000: 
                    original_csv_df.drop(original_csv_df.tail(1).index,axis=0, inplace=True)
                    unique_channels = original_csv_df['channel_id'].nunique()
                    rows_dropped += 1
                    pbar.update(1)

                pbar.close()
                print("-"*10)
                print("Deleted {} number of rows".format(rows_dropped))

            print("-"*20)
            print("Fetching Youtube channel stats...")


            channel_stats_dict = yt_api_channel(youtube,original_csv_df)
            columns = ['channel_view_total','channel_subscriber_total','channel_video_total']

            for column in columns:
                original_csv_df[column] = channel_stats_dict[column]

            original_csv_df.to_csv(r'export/youtube-dataset-channel.csv',index=None)

        elif option == 'video stats':
            yt_df = pd.read_csv('export/youtube-dataset-channel.csv')

            unique_videos = yt_df['video_id'].nunique()

            if unique_videos > 10000:
                print("Due to API quota, your dataset is too large.")
                rows_dropped = 0
                pbar = tqdm(total= abs(unique_videos-10000))

                while unique_videos > 10000: 
                    yt_df.drop(yt_df.tail(1).index,axis=0, inplace=True)
                    unique_videos = yt_df['video_id'].nunique()
                    rows_dropped += 1
                    pbar.update(1)

                pbar.close()
                print("-"*10)
                print("Deleted {} number of rows".format(rows_dropped))

            print("-"*20)
            print("Fetching Youtube video stats...")

            video_stats = yt_api_video(youtube,yt_df)
            columns = ['video_view_total','video_like_total','video_comment_total','video_topics']

            for column in columns:
                yt_df[column] = video_stats[column]

            yt_df.head()
            yt_df.to_csv (r'export/watch-history-full.csv', index = None)
        
        print("\n")
        option = menu()
