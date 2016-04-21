import json
import os
import telepot
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
from slugify import slugify

TOKEN = '#########:###################################'
WelcomeGreeting = 'Welcome! Just send me the name of the song that you want to download.'
base_url = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video='

def handleBotMessage(msg):
    print 'handing message...'
    chat_id = msg['from']['id']
    command = msg['text']
    username = msg['from']['first_name']
    print 'Request accepted'

    if command == '/start':
        bot.sendMessage(chat_id, WelcomeGreeting)
        return

    song_name = command
    bot.sendMessage(chat_id, 'Hi '+username+', the song \"'+song_name+'\" is on its way...')

    query = urllib.quote(song_name+ "song")
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)

    soup = BeautifulSoup(response.read(), "html.parser")
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        video_url = 'https://www.youtube.com' + vid['href']
        print ('Video url: ' + video_url)
        json_url = base_url + video_url
        print ('Json url: ' + json_url)

        response = urllib.urlopen(json_url)

        try:
            data = json.loads(response.read())
            if 'length' not in data:
                raise ValueError("No length present.")
                break
            if 'link' not in data:
                raise ValueError("No link present.")
                break
            if 'title' not in data:
                raise ValueError("No title present.")
                break

            length = data['length']
            downLoad_url = data['link']
            title = data['title']
            print ('length: ' + str(length))
            print ('download url: ' + downLoad_url)
            print ('title: ' + title)

            upload_file = path + slugify(title).lower() + '.mp3'
            print ('upload_file name : ' + upload_file)

            if not (os.path.exists(upload_file)) :
                bot.sendMessage(chat_id, 'Download for your song has started..')
                print ('Downloading song to Bot collection.')

                downloadSong(downLoad_url, upload_file)
                bot.sendMessage(chat_id, 'Download is complete. Song is being sent to you. Please wait.')
                print ('Download is complete.')
            else:
                print ('Song is already present in Bot collection.')

            print ('Sending song')

            bot.sendAudio(chat_id, open(upload_file , 'rb'), length , '', title)

            print ('Sent successfully!')

        except ValueError as e:
            print 'No song found', e
            bot.sendMessage(chat_id, 'No song found. Please try again with a different keyword.')

        break

def downloadSong(url, fileLoc):
    f = open(fileLoc, 'wb')
    usock = urllib2.urlopen(url)
    try :
      file_size = int(usock.info().getheaders("Content-Length")[0])
      print ('Downloading: %s Bytes: %s' % (fileLoc, file_size))
    except IndexError:
      print ('Unknown file size: index error')

    block_size = 8192
    while True:
        buff = usock.read(block_size)
        if not buff:
            break
        f.write(buff)
    f.close()

    print "done"

bot = telepot.Bot(TOKEN)
bot.notifyOnMessage(handleBotMessage)
print 'Listening...'

path = '/Users/apoorvam/Downloads/Bot/'

# Keep the program running
while 1:
    time.sleep(10)
