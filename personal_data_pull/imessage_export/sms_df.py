import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from hashlib import sha1
import yaml

QUERY = """
    SELECT 
        message.date AS apple_timestamp,
        message.text,
        message.is_from_me,
        handle.id AS handle,
        chat.ROWID AS chat,
        attachment.filename AS attachment_filename,
        attachment.mime_type AS attachment_mime_type
    FROM
        message 
            LEFT JOIN chat_message_join ON chat_message_join.message_id=message.ROWID
            LEFT JOIN chat ON chat.ROWID=chat_message_join.chat_id
            LEFT JOIN message_attachment_join ON message_attachment_join.message_id=message.ROWID
            LEFT JOIN attachment ON message_attachment_join.attachment_id=attachment.ROWID
            LEFT JOIN chat_handle_join ON chat.ROWID=chat_handle_join.chat_id
            LEFT JOIN handle ON chat_handle_join.handle_id=handle.ROWID
    ORDER BY 
        message.date desc
"""

BACKUP_ROOT = Path(
    "/Users/chrisp/Library/Application Support/MobileSync/" +
    "Backup/c249fba721f82e9cafdaa59ff4e004c2af39501e"
)

def apple_timestamp_to_datetime(apple_timestamp):
    return datetime.fromtimestamp(apple_timestamp / 1000000000 + 978307200)

def get_hashed_fs_path(path):
    if path:
        hashable_path = "MediaDomain-" + str(Path(path).resolve().relative_to(Path('~').resolve()))
        print(hashable_path)
        hashed_path = sha1(hashable_path.encode('utf-8')).hexdigest()
        print(hashed_path)
        return BACKUP_ROOT / 'Snapshot' / hashed_path[:2] / hashed_path

def get_sms_df(db_file):
    connection = sqlite3.connect(db_file)
    df = pd.read_sql_query(QUERY, connection)
    df['date'] = df.apple_timestamp.map(apple_timestamp_to_datetime)
    handles = yaml.safe_load(Path('handles.yaml').read_text())
    df['contact'] = df.handle.map(handles)
    df = df.sort_values('date')
    #df['attachment_path'] = df.attachment_filename.map(get_hashed_fs_path)
    return df
