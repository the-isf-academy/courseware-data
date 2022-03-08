from sms_df import get_sms_df
from pathlib import Path
from format_sms import HEADER, format_chat
import shutil
import os

DB = "data/chat.db"
EXPORT_DIR = Path("./export")
OUTFILE = "sms.html"

def copy_messages_db_from_library():
    return os.system('cp /Users/$(whoami)/Library/Messages/chat.db data/')
    
def export_sms_to_html():
    df = get_sms_df(DB)
    df.to_csv(EXPORT_DIR / "imessage.csv")
    # html = HEADER
    # for chat, messages in df.groupby("chat"):
        # html += format_chat(messages)
    # (EXPORT_DIR / "index.html").write_text(html)

if __name__ == '__main__':
    if copy_messages_db_from_library():
        print("Can't find your iMessages database. You may need to backup your messages and manually add the database to this directory.")
    export_sms_to_html()
