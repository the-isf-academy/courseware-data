import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from hashlib import sha1
import yaml


def get_whatsapp_df(chat_file, datetime_format="%m/%d/%Y, %X"):
    print(chat_file)
    with chat_file.open() as f:
        lines = f.readlines()
        parsed_lines = []
        for line in lines:
            line_valid = True
            line = line.strip('\u200e')
            print(line)
            if ' end-to-end encrypted' in line:
                print('invalid', line)
                line_valid = False
            elif line[0] != '[':
                # print(line)
                same_msg = list(parsed_lines[-1])
                same_msg[-1] += " " + line
                # print(same_msg)
            else:
                parsed_line = parse_line(line, datetime_format)
                if parsed_line:
                    parsed_lines.append(parsed_line)
                # print(parsed_line[0].split(',')[1])
        # print(parsed_line)
        if line_valid:
            df = pd.concat([pd.DataFrame({'date':[date],'time':[time],'sender':[sender], 'message':[message]}) for date, time, sender, message in parsed_lines])
    df = df.sort_values('date')
    return df

def get_whatsapp_df_nozip(chat_file, datetime_format="%m/%d/%Y, %X"):
    with open(chat_file) as f:
        lines = f.readlines()
        parsed_lines = []
        for line in lines:
            line = line.strip('\u200e')
            # print(line)
            
            if ':' in line or len(line) ==0:
                pass
           
            elif line[0] != '[':
                if len(parsed_lines) > 0:
                    same_msg = list(parsed_lines[-1])
                    same_msg[-1] += " " + line
                # print(same_msg)
            else:
                print(line)
                parsed_line = parse_line(line, datetime_format)
                if parsed_line:
                    parsed_lines.append(parsed_line)
                # print(parsed_line[0].split(',')[1])
        print(parsed_lines)
        df = pd.concat([pd.DataFrame({'date':[date], 'sender':[sender], 'message':[message]}) for date, sender, message in parsed_lines])
    df = df.sort_values('date')
    return df


def parse_line(line, datetime_format):
    if line.count(":") >= 3:
        # print(line)
        split_line = line.split(':', 3)
        meta_data =  (':').join(split_line[:3])
        message = split_line[-1].strip().strip('\u200e')
        date, name = meta_data.split('] ')
        date = date.strip('[')

        date,time = date.split(',')
        time = time.replace(' ','')
        print('date',date)

        if "am" in time or "pm" in time or 'AM' in time or 'PM' in time:
            if 'pm' in time or 'PM' in time:
                # print(len(time[:time.index(":")]))
                # if len(time[:time.index(":")]) == 2:
                    # print(time[:time.index(":")])
                new_hour = int(time[:time.index(":")]) + 12
                time = str(new_hour) + time[time.index(":"):]

            time = time[:-2]
    
        print(name)
        name = name.strip()
        # print(date)
        return (date, time, name, message)
    else:
        return False



