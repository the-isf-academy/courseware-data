# Exporting SMS
These scripts attempt to find your iMessage data and export it to a CSV file for use in data analysis.

## Installation
First, install the packages these scripts require:
```
pip install requirements.txt
```

## Running the script
Run this script using the following command:
```
python export_sms.py
```

You can find your data in the `exports/` directory.

### Contact names
iMessage data is stored without associating a handle (phone number or
email address) with a contact name. If you would like to add contact names
to your data, you can add these mappings to `handles.yaml` in the following
format:
```
"+12345678910": "Phone Contact Name"
"email_address@email.com": "Email Contact Name"
```

### iMessages from a backup
This script should work automatically if you are using MacOS and have iMessage data synced across your devices. If your
iMessage data is not on your computer, you can also make these scripts work by manually adding your iMessage chat database
to `data/chats.db`.

Here are instructions for how to do this:
TODO
