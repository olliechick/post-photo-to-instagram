import csv
import json
import os
import random
import urllib.request
from datetime import datetime, timedelta
import requests
import sentry_sdk
from instabot import Bot

PLACEHOLDER = "placeholder"
IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]
VIDEO_EXTENSIONS = ["mp4", "mov"]

ENV_TRUSTIFI_URL = 'TRUSTIFI_URL'
ENV_TRUSTIFI_KEY = 'TRUSTIFI_KEY'
ENV_TRUSTIFI_SECRET = 'TRUSTIFI_SECRET'
ENV_SENTRY_DSN = 'SENTRY_DSN'

ENV_USERNAME = 'ig_username'
ENV_PASSWORD = 'ig_password'
ENV_INPUT_URL = 'input_url'
ENC_INPUT_URL_ENCODING = 'input_url_encoding'
ENV_IMAGE_HOST = 'image_host'
ENV_USE_SAME_DATE = 'same_date'
ENV_POST_PHOTO_TO_INSTAGRAM_MODE = 'ppti_mode'
ENV_TO_EMAIL = 'ppti_to_email'
ENV_TO_NAME = 'ppti_to_name'

MODE_INSTAGRAM = 'instagram'
MODE_EMAIL = 'email'
MODE_ALL = 'all'


def get_extension(filename):
    return filename.split('.')[-1]


def excel_date_to_datetime(excel_date):
    temp = datetime(1889, 12, 31)
    delta = timedelta(days=excel_date)
    return temp + delta


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


def get_random_post(posts, use_same_date_if_possible):
    if use_same_date_if_possible:
        valid_posts = []
        today = datetime.now()
        for post in posts:
            if len(post) > 2:
                date_str = post[2]
                date = False
                if '-' in date_str:
                    date = datetime.strptime(date_str, '%d-%b-%y')
                elif date_str:
                    date = excel_date_to_datetime(float(date_str))
                if date and date.day == today.day and date.month == today.month:
                    valid_posts.append(post)
        if len(valid_posts):
            posts = valid_posts
    i = random.randrange(len(posts))
    post = posts[i]
    filename = post[0]
    caption = post[1]
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
    use_same_date_if_possible = ENV_USE_SAME_DATE in os.environ and os.environ[ENV_USE_SAME_DATE] == 'true'
    media_url, placeholder_filename, caption = get_random_post(posts, use_same_date_if_possible)

    mode = MODE_INSTAGRAM
    if ENV_POST_PHOTO_TO_INSTAGRAM_MODE in os.environ:
        mode = os.environ[ENV_POST_PHOTO_TO_INSTAGRAM_MODE]

    if mode == MODE_EMAIL or mode == MODE_ALL:
        url = os.environ[ENV_TRUSTIFI_URL] + '/api/i/v1/email'

        payload = json.dumps({
            "recipients": [
                {
                    "email": os.environ[ENV_TO_EMAIL],
                    "name": os.environ[ENV_TO_NAME],
                }
            ],
            "lists": [],
            "contacts": [],
            "attachments": [],
            "title": "Automated Instagram post",
            "html": f"{caption}<br /><a href=\"{media_url}\">link</a>",
            "methods": {
                "postmark": False,
                "secureSend": False,
                "encryptContent": False,
                "secureReply": False
            },
            "from": {"name": os.environ[ENV_TO_NAME]}
        })

        headers = {
            'x-trustifi-key': os.environ[ENV_TRUSTIFI_KEY],
            'x-trustifi-secret': os.environ[ENV_TRUSTIFI_SECRET],
            'Content-Type': 'application/json'
        }

        response = requests.request('POST', url, headers=headers, data=payload)
        print(response.json())

    elif mode == MODE_INSTAGRAM or mode == MODE_ALL:
        # Download media
        print("Downloading " + media_url)
        try:
            urllib.request.urlretrieve(media_url, placeholder_filename)
        except Exception as e1:
            try:
                urllib.request.urlretrieve(media_url, placeholder_filename)
            except Exception as e2:
                raise Exception(f"Errors while downloading image from {media_url}: {e1}, {e2}")

        # Set up Instabot
        bot = Bot()
        bot.login(username=os.environ[ENV_USERNAME], password=os.environ[ENV_PASSWORD])

        # Upload media
        print("Uploading post with caption: " + caption)
        upload_media(bot, placeholder_filename, caption)
        os.remove(placeholder_filename)


if __name__ == '__main__':
    main()
