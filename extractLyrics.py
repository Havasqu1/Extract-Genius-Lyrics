import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import ast
import os
from urllib.request import Request, urlopen

# For ignoring SSL certificate errors

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Input from user
url = input('input url')

# Making the website believe that you are accessing it using a mozilla browser
req = Request(url, headers = { 'User-Agent' : 'Mozilla/5.0' })
webpage = urlopen(req).read()

# Creating a BeautifulSoup object of the html page for easy extraction of data.

soup = BeautifulSoup(webpage, 'html.parser')
html = soup.prettify('utf-8')
song_json = {}
song_json["Lyrics"] = []
song_json["Comments"] = []

#Extract Title of the song
for title in soup.findAll('title'):
    song_json["Title"] = title.text.strip()

# Extract the release date of the song
for span in soup.findAll('span', attrs = {'class': 'metadata_unit-info metadata_unit-info--text_only'}):
    song_json["Release date"] = span.text.strip()

# Extract the Comments on the song
for div in soup.findAll('div', attrs = {'class': 'rich_text_formatting'}):
    comments = div.text.strip().split("\n")
    for comment in comments:
        if comment!="":
            song_json["Comments"].append(comment)

#Extract the Lyrics of the song
for div in soup.findAll('div', attrs = {'class': 'lyrics'}):
    song_json["Lyrics"].append(div.text.strip().split("\n"))

#Save the json created with the file name as title + .json
with open(song_json["Title"] + '.json', 'w') as outfile:
    json.dump(song_json, outfile, indent = 4, ensure_ascii = False)

# Save the html content into an html file with name as title + .html
with open(song_json["Title"] + '.html', 'wb') as file:
    file.write(html)