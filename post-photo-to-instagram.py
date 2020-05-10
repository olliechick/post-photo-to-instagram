import os
import sys
import urllib.request

import requests
from instabot import Bot

IMAGE_FILENAME = "image.jpg"


def main():
    sys.path.append(os.path.join(sys.path[0], "../../"))

    link = input("Enter image URL: ")
    f = requests.get(link)
    image_url, caption = f.text.split('\n')

    # Download today's image

    try:
        urllib.request.urlretrieve(image_url, IMAGE_FILENAME)
    except Exception as e1:
        try:
            urllib.request.urlretrieve(image_url, IMAGE_FILENAME)
        except Exception as e2:
            print(f"Errors while downloading image': {e1}, {e2}")

    bot = Bot()
    bot.login()

    pic = IMAGE_FILENAME

    try:
        print("Uploading " + caption)

        bot.upload_photo(pic, caption=caption)
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
