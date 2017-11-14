#!/usr/bin/env python3
#
# image-grabber
#
# A python script for downloading images from popular websites.
#
# Uses URL from either an optional argument or the clipboard.

# to handle command line arguments
import sys
# clipboard access
import pyperclip
# for downloading data from the web
import requests
# for extracting information from html
import bs4
# for navigating json responses
import json
# for making directories to store images
import os

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
image_count = 0


def check(address):
    if type(address) == str:
        # link points to an image
        #any() checks a list of conditions; We're checking for any one extension in the address
        if any(ext in address for ext in ['.jpg','.jpeg','.tiff','.gif','.bmp','.png','.bat','.gifv','.webm','.mp4']):
            # make directory for images
            os.makedirs('pictures', exist_ok = True)
            download_and_save(address)
            # image counter
            global image_count 
            image_count += 1
            # invalid address
        elif address[:4] != 'http':
            print('Invalid address')
        # link points to a web page
        else:
            # request the URL
            response = requests.get(address, headers = {'User-agent': 'your bot 0.1'})
            # check if an error is raised
            try:
                response.raise_for_status()
                # pass text attribute to bs4 object using lxml parser
                text = bs4.BeautifulSoup(response.text, "lxml")
                # check against supported websites
                if 'google.' in address:
                    check(googleimages(address))
                elif 'imgur.com' in address:
                    check(imgur(address))
                elif 'reddit.com' in address:
                    check(reddit(text))
                else:
                    print('Site not yet supported:', address)
            except requests.exceptions.HTTPError:
                print('404 Client Error:', address, 'Not Found.')
    # image list
    elif type(address) == list:
        for sub_address in address:
            check(sub_address)
    return None


# function for downloading and saving on disk
def download_and_save(address):
    #We're checking if file extension has ? appended; if so, we're removing excess text to save with valid filename
    if any(ext in address for ext in ['.jpg?','.jpeg?','.tiff?','.gif?','.bmp?','.png?','.bat?','.gifv?','.webm?','.mp4?']):
        filename = address[:address.rfind('?')]
    else:
        filename = address
    # download image
    print('Downloading image', os.path.basename(filename))
    image = requests.get(address, headers = {'User-agent': user_agent})
    image.raise_for_status()
    image_file = open(os.path.join('pictures', os.path.basename(filename)), 'wb')
    # save image
    for chunk in image.iter_content(100000):
        image_file.write(chunk)
    image_file.close()
    print('Saved!')
    return None


# images.google.com support
def googleimages(address):
    # create a list of image links
    image_links = []
    # create new URL
    new_link = 'https://www.google.com/search?q=' + address[address.find('=') +
        1:address.find('&')] + '&source=lnms&tbm=isch'

    try:
        response = requests.get(new_link, headers={'User-agent': user_agent})
        # get result page
        page = bs4.BeautifulSoup(response.text, "lxml")
        # collect images from page
        thumbs = page.find_all(attrs={'class':'rg_meta notranslate'})
        json_strs = [thumb.string for thumb in thumbs]
        for json_str in json_strs:
            j_obj = json.loads(json_str)
            image_links.append(j_obj['ou'])
    except requests.exceptions.HTTPError:
        print('404 Client Error:', address, 'Not Found.')

    return image_links


# imgur.com support
def imgur(address):
    # create a list of image links
    image_links = []
    if not 'ajax' in address:
        # collect album id
        id = address[-5:]
        # make new URL
        address = 'http://imgur.com/ajaxalbums/getimages/' + id + '/hit.json?all=true'
    # request the URL
    response = requests.get(address, headers={'User-agent': user_agent})
    try:
        response.raise_for_status()
        image_list = json.loads(response.text)
        # create list of image parameters
        for image in image_list['data']['images']:
            image_id = image['hash']
            image_ext = image['ext']
            image_links.append("https://i.imgur.com/" + image_id + image_ext)
    except requests.exceptions.HTTPError:
        print('404 Client Error:', address, 'Not Found.')
    return image_links


# reddit.com support
def reddit(text):
    # identify full image URLs
    posts = text.select('div[data-url]')
    # a list of the image links
    image_links = []
    # collect all available posts
    for index in range(len(posts)):
        image_links.append(posts[index].get('data-url'))
    print(len(image_links), 'posts found.')
    print('')
    return image_links


# act according to the presence of an argument (URL)
if len(sys.argv) > 1:
    # get address from argument
    address = sys.argv[1]
else:
    try:
        # get address from clipboard
        address = pyperclip.paste()
        print('')
        print('Address taken from clipboard.')
    except AssertionError:
        # kde causes issues due to two user interfaces for klipper
        # https://forum.kde.org/viewtopic.php?f=289&t=135553
        print('')
        print('You might need to install xclip.')
        print('')
        sys.exit()


# request address
print('')
print('Downloading page:', address)
print('')
# run downloader
check(address)
print('')
print(image_count, 'images downloaded.')
print('')
