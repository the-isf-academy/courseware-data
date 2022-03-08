from pathlib import Path
import yaml

HEADER = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Helvetica; }
    h2 { text-align: center; font-size: 1.2em; margin-top: 10px;}
    img { width: 100%; }
    video { width: 100%; }
    .conversation { max-width: 800px; margin: 0 auto; }
    .message { display: flex; margin: 10px 0;}
    .date { width: 150px; color: #888; }
    .me { 
      margin: 5px 30% 5px 5px; 
      text-align: left; 
      flex: 1 1; 
      overflow: hidden; border: 
    }
    .you {
      margin: 5px 5px 5px 30%; 
      text-align: right; 
      flex: 1 1; 
      overflow: hidden;
    }
  </style>
</head>
"""

handles = yaml.safe_load(Path('handles.yaml').read_text())

def format_chat(messages):
    html = '<hr><div class="conversation">'
    names = [handles.get(h, h) for h in messages.handle.unique()]
    html += '<h1>{}</h1>'.format(', '.join(names))
    for date, day_messages in messages.groupby('date', as_index=False).first().resample('D', on='date'):
        if len(day_messages):
            html += "<h2>{}</h2>".format(date.strftime("%B %d, %Y"))
            for ix, msg in day_messages.iterrows():
                html += format_message(msg)
    html += '</div>'
    return html

def convert_attachment_path(p):
    base = "~/Library/SMS/Attachments"
    if not (p and p.startswith(base)):
        return None
    relpath = Path(p).relative_to(Path(base))
    return "media/" + str(relpath)

def format_message(msg):
    html = '<div class="message"><div class="date">{}<br>{}</div><div class="{}">'.format(
        'Me' if msg.is_from_me else handles.get(msg.handle, msg.handle),
        msg.date.strftime("%-I:%M%p"),
        'me' if msg.is_from_me else 'you',
    )
    attachment_path = convert_attachment_path(msg.attachment_filename)
    if attachment_path and msg.attachment_mime_type:
        if msg.attachment_mime_type.startswith("image"):
            html += '<img src="{}">'.format(attachment_path)
        elif msg.attachment_mime_type.startswith("video"):
            html += '<video controls><source src="{}"></video>'.format(attachment_path)
    html += (msg.text.replace('￼', '') if msg.text else '') + "</div></div>"
    return html
