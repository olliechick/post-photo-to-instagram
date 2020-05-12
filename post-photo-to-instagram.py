import csv
import os
import random
import urllib.request
from datetime import date

import requests
from instabot import Bot

IMAGE_FILENAME = "image.jpg"


def main():

    # Get image URL
    posts = csv.reader(requests.get(os.environ['input_url']).text.splitlines())
    random.seed(date.today())
    i = random.randrange(len(posts))
    filename, caption = posts[i]
    image_url = os.environ['image_host'] + filename

    # Download image
    try:
        urllib.request.urlretrieve(image_url, IMAGE_FILENAME)
    except Exception as e1:
        try:
            urllib.request.urlretrieve(image_url, IMAGE_FILENAME)
        except Exception as e2:
            print(f"Errors while downloading image': {e1}, {e2}")

    bot = Bot()
    bot.login(username=os.environ['ig_username'], password=os.environ['ig_password'])

    pic = IMAGE_FILENAME

    try:
        print("Uploading post with caption: " + caption)

        bot.upload_photo(pic, caption=caption)
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)

        os.remove(IMAGE_FILENAME + ".REMOVE_ME")

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
