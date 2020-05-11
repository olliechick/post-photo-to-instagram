import os
import sys
import urllib.request

import requests
from instabot import Bot

IMAGE_FILENAME = "image.jpg"


def main():
    sys.path.append(os.path.join(sys.path[0], "../../"))

    link = os.environ['input_url']
    f = requests.get(link)
    output = f.text.split('\n')
    image_url = output[0]
    caption = '\n'.join(output[1:])

    # Download today's image

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
        print("Uploading " + caption)

        bot.upload_photo(pic, caption=caption)
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)

        os.remove(IMAGE_FILENAME + ".REMOVE_ME")

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
