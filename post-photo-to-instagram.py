import csv
import os
import random
import urllib.request
from datetime import date

import requests
from instabot import Bot

PLACEHOLDER = "placeholder"


def main():
    # Get image URL
    reader = csv.reader(requests.get(os.environ['input_url']).text.splitlines())
    posts = []
    for post in reader:
        posts.append(post)

    random.seed(date.today())
    i = random.randrange(len(posts))
    print(posts[i])
    filename, caption = posts[i]
    image_url = os.environ['image_host'] + filename
    extension = filename.split('.')[-1]

    placeholder_filename = f"{PLACEHOLDER}.{extension}"

    # Download image
    try:
        urllib.request.urlretrieve(image_url, placeholder_filename)
    except Exception as e1:
        try:
            urllib.request.urlretrieve(image_url, placeholder_filename)
        except Exception as e2:
            print(f"Errors while downloading image': {e1}, {e2}")

    bot = Bot()
    bot.login(username=os.environ['ig_username'], password=os.environ['ig_password'])

    try:
        print("Uploading post with caption: " + caption)

        bot.upload_photo(placeholder_filename, caption=caption)
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)

        os.remove(placeholder_filename + ".REMOVE_ME")

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
