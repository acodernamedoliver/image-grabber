# image-grabber
A python script for downloading images from popular websites.

## Description
__image-grabber__ takes a URL and proceeds to download all image from the given website. It can work recursively for supported websites, i.e. for posts on reddit that have images hosted on imgur as albums, all images from that album will be downloaded.

The URL can be either provided as an argument on the command line inside quotes, or can be taken automatically from the clipboard.

Images are stored inside a folder named "pictures", which is created in the same directory the script is stored in.

## Usage
__image-grabber__ uses Python3. To use it, navigate to the directory the script is in and type the following:

```
python3 script.py <URL>
```

## Website support
- reddit
- imgur

## TODO
### Add support for:
- google images
- flickr
- you tell me :blush:

### Other:
- provide option for custom directory
