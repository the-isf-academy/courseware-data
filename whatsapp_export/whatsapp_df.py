import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from hashlib import sha1
import yaml


def get_whatsapp_df(chat_file, datetime_format="%m/%d/%Y, %X"):
    with chat_file.open() as f:
        lines = f.readlines()
        parsed_lines = []
        for line in lines:
            parsed_line = parse_line(line, datetime_format)
            if parsed_line:
                parsed_lines.append(parsed_line)
                # print(parsed_line[0].split(',')[1])
        df = pd.concat([pd.DataFrame({'date':[date.split(',')[0]],'time':[date.split(',')[1]], 'sender':[sender], 'message':[message]}) for date, sender, message in parsed_lines])
    df = df.sort_values('date')
    return df


def parse_line(line, datetime_format):
    line = line.strip('\u200e')
    if line.count(":") >= 3:
        split_line = line.split(':', 3)
        meta_data =  (':').join(split_line[:3])
        message = split_line[-1].strip().strip('\u200e')
        date, name = meta_data.split(']')
        date = date.strip('[')
        # print(date)
        if "am" or "pm" in date:
            new_date_format = datetime_format + "%I:%M:%S %p"
            date = datetime.strftime(
                datetime.strptime(date, new_date_format),
                    datetime_format + " %H:%M:%S")
        else:
            date = datetime.strptime(date, datetime_format + " %H:%M:%S")
        name = name.strip()
        # print(date)
        return (date, name, message)
    else:
        return False



