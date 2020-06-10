# Post photo to Instagram
Post a randomly-selected photo to Instagram from a list of available photos.

Videos can also be posted, but this has not been fully tested so may not work.

## Instructions

### Setup

Install packages from `requirements.txt`.

Host a CSV file on a website of all the possible photos in the format `filename,caption`, for example:

```csv
'image1.jpg','My caption'
```

These images should be hosted on a website with the filenames matching those in the CSV file.

Create the following environment variables:

| Environment variable | Description        | Example    |
|----------------------|--------------------|------------|
| `ig_username`        | Instagram username | `username` |
| `ig_password`        | Instagram password | `password` |
| `input_url`          | URL of CSV file    | `https://olliechick.co.nz/example.csv` |
| `input_url_encoding` |Encoding of CSV file| `utf-8-sig`                            |
| `image_host`         | Base URL of images | `https://olliechick.co.nz/ig_media/`   |

In the examples given, there is an image at https://olliechick.co.nz/ig_media/image1.jpg, which will be posted with the caption "My caption".

#### Sentry

If you have connected [Sentry](https://docs.sentry.io/) to the application, this will receive any exceptions raised. The environment variable `SENTRY_DSN` should be set to the DSN provided by Sentry.

### Running

When run, the program will post a random photo from those listed in the CSV file.

Instagram may block the login attempt if, for example, you have a new account or you run it from a server hosted in another country to the one that you normally logged in to your account on. The API this runs on recommends you not use your own account.

Note that the random number generated to decide which image to post is an independent event - don't fall victim to the [Gambler's fallacy](https://en.wikipedia.org/wiki/Gambler%27s_fallacy).