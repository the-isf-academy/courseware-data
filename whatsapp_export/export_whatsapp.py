from whatsapp_df import get_whatsapp_df, get_whatsapp_df_nozip
from pathlib import Path
import shutil
import os
from pathlib import Path
import tempfile
import zipfile
import pandas as pd
import glob

from simple_term_menu import TerminalMenu

DATA_DIR = "data"
EXPORT_DIR = Path("./export")
OUTFILE = "whatsapp.csv"
DATETIME_FORMAT = "%m/%d/%Y, %X"

def get_chat_df(zipped_chat):
    with tempfile.TemporaryDirectory() as tmp_chat_dir:
        tmp_submission_dir = Path(tmp_chat_dir)
        with zipfile.ZipFile(zipped_chat, mode='r') as zip_ref:
            chat_file = (zipfile.Path(zip_ref) / "_chat.txt")
            df = get_whatsapp_df(chat_file, DATETIME_FORMAT)
            chat_name = zip_ref.filename.split(" - ")[1].split(".")[0] 
            df['chat_name'] = chat_name
            return df

def get_chat_nozip_df(zipped_chat):
    chat_file = glob.glob("data/*.txt")[0]
    print(chat_file)
    df = get_whatsapp_df_nozip(chat_file, DATETIME_FORMAT)
    
    chat_name = chat_file.split(" - ")[1].split(".")[0] 
    df['chat_name'] = chat_name
    return df

def export_whatsapp_to_csv():
    chat_dfs_list = []
    data_dir = Path(DATA_DIR)
    for child in data_dir.iterdir():
        # print(child)
        if child.suffix == ".zip":
                df = get_chat_df(child)
                chat_dfs_list.append(df)
        # else:
        #     df = get_chat_nozip_df(child)
        #     chat_dfs_list.append(df)
    chat_dfs = pd.concat(chat_dfs_list)
    chat_dfs = chat_dfs.sort_values('date')
    chat_dfs.to_csv(EXPORT_DIR / "whatsapp.csv")

if __name__ == '__main__':
    datetime_dict = {"DD/MM/YYYY": "%d/%m/%Y","MM/DD/YYYY": "%m/%d/%Y"}
    date_format_menu = TerminalMenu(datetime_dict.keys(), title="Select date format of your chat data:")
    menu_entry_index = date_format_menu.show()
    DATETIME_FORMAT = datetime_dict[list(datetime_dict.keys())[menu_entry_index]]
    export_whatsapp_to_csv()

    print("----- Finished Export -----")
    print(".csv file can be found in /export")
    print("-"*30)
