import csv
import os
import random
import urllib.request

import requests
import sentry_sdk
from instabot import Bot

PLACEHOLDER = "placeholder"
IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]
VIDEO_EXTENSIONS = ["mp4", "mov"]

ENV_USERNAME = 'ig_username'
ENV_PASSWORD = 'ig_password'
ENV_INPUT_URL = 'input_url'
ENC_INPUT_URL_ENCODING = 'input_url_encoding'
ENV_IMAGE_HOST = 'image_host'
ENV_SENTRY_DSN = 'SENTRY_DSN'


def get_extension(filename):
    return filename.split('.')[-1]


def get_posts():
    request = requests.get(os.environ[ENV_INPUT_URL])
    if ENC_INPUT_URL_ENCODING in os.environ:
        request.encoding = os.environ[ENC_INPUT_URL_ENCODING]
    reader = csv.reader(request.text.splitlines())
    posts = []
    for post in reader:
        if len(post) > 0:
            posts.append(post)
    return posts


def get_random_post(posts):
    i = random.randrange(len(posts))
    filename, caption = posts[i]
    media_url = os.environ[ENV_IMAGE_HOST] + filename
    placeholder_filename = f"{PLACEHOLDER}.{get_extension(filename)}"
    return media_url, placeholder_filename, caption


def upload_media(bot, filename, caption):
    extension = get_extension(filename)
    if extension in IMAGE_EXTENSIONS:
        bot.upload_photo(filename, caption=caption, options={"rename": False})
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)
            raise Exception("Post not posted")
    elif extension in VIDEO_EXTENSIONS:
        bot.logger.info("Checking {}".format(filename))
        if not bot.upload_video(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), filename),
                caption=caption, options={"rename": False}
        ):
            raise Exception("Something went wrong when uploading the video: " + filename)
        bot.logger.info("Successfully uploaded: " + filename)
        return
    else:
        raise Exception(f"Error: {extension} not supported.")


def main():
    if ENV_SENTRY_DSN in os.environ:
        sentry_sdk.init(os.environ[ENV_SENTRY_DSN])

    posts = get_posts()
    media_url, placeholder_filename, caption = get_random_post(posts)

    # Download media
    try:
        urllib.request.urlretrieve(media_url, placeholder_filename)
    except Exception as e1:
        try:
            urllib.request.urlretrieve(media_url, placeholder_filename)
        except Exception as e2:
            raise Exception(f"Errors while downloading image': {e1}, {e2}")

    # Set up Instabot
    bot = Bot()
    bot.login(username=os.environ[ENV_USERNAME], password=os.environ[ENV_PASSWORD])

    # Upload media
    print("Uploading post with caption: " + caption)
    upload_media(bot, placeholder_filename, caption)
    os.remove(placeholder_filename)


if __name__ == '__main__':
    main()
