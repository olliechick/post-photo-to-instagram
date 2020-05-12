# Post photo to Instagram
Post a randomly-selected photo (or video) to Instagram from a list of available photos.

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
| `image_host`         | Base URL of images | `https://olliechick.co.nz/ig_media/`   |

In the examples given, there is an image at https://olliechick.co.nz/ig_media/image1.jpg.

### Running

When run, the program will post a random photo from those listed in the CSV file.
The seed for the randomness is the current day, so running this multiple times in the same day will result in the same image posted.
Also note that the random number generated is an independent event - don't fall victim to the [Gambler's fallacy](https://en.wikipedia.org/wiki/Gambler%27s_fallacy).