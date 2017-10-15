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
# for making directories to store images
import os

def check(address):
    if type(address) == str:
        # link points to an image
        if ('.jpg' in address or '.jpeg' in address or '.tiff' in address or '.gif' in address or '.bmp' in address or '.png' in address or '.bat' in address):
            # make directory for images
            os.makedirs('pictures', exist_ok = True)
            download_and_save(address)
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
                if 'reddit.com' in address:
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
    # download image
    print('Downloading image', os.path.basename(address))
    image = requests.get(address, headers = {'User-agent': 'your bot 0.1'})
    image.raise_for_status
    image_file = open(os.path.join('pictures', os.path.basename(address)), 'wb')
    # save image
    for chunk in image.iter_content(100000):
        image_file.write(chunk)
    image_file.close()
    print('Saved!')
    return None

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

check(address)

print('')
