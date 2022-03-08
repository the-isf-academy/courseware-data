# Exporting Whatsapp Chats
These scripts transform Whatsapp chat export files into a csv file.

## Installation
First, install the packages these scripts require:
```
pip install requirements.txt
```

## Add Whatsapp chat file
To use this, you will need to export your Whatsapp chats and add them to the `data/` directory.

- To export a Whataspp chat, open the Whatsapp app on your phone, and open a chat.
- Open the chat settings by clicking the name of the chat at the top of the screen.
- Scroll down and select "Export Chat."
- Transfer the file to your computer and place it in the `data/` directory of this package.

Note: This script expects chat files as `.zip` files. Do not unzip or rename the file. Just
put it in the `data\` directory exactly how it gets exported from Whatsapp.

You can add as many chat files as you want.

## Running the script
Run this script using the following command:
```
python3 export_whatsapp.py
```

**You can find your data in the `exports/` directory.**

## Group chats and chat names
This script records who sent a message and what chat the message was sent to.

In the case of group chats, this means that each entry in the resulting csv file
will show who sent the message and what group the message was sent to.

In the case of one-to-one chats, the chat name will be the name of the person
you chatted with. Thus, each entry will show who sent a message (you or the other
person) and the other person's name as the chat name.
