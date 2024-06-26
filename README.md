# Imot crawler

A crawler for the `imot.bg` and `imoti.com` websites.

## Running

1. Create virtual environment for the project using Python 3.8+
2. Install requirements with `pip install -r requirements.txt`
3. Copy `imot_bg_crawler/input.example.yaml` to `imot_bg_crawler/input.yaml` and update the search
   URLs in the file. When done, check with `http://www.yamllint.com/` if the input file is okay.
4. Copy `imot_bg_crawler/settings.example.py` to `imot_bg_crawler/settings.py` and change the settings
   as you need them _(see the [Settings](#settings) section)_.
5. Run spider for the desired website. If you do not want logs add `--nolog` in the end of the command
6. When finished, check the `./imot_bg_crawler/output_files` folder for the results.
7. Enjoy.


## Spiders

1. Imot.bg - `scrapy crawl imot.bg`
2. Imoti.com - `scrapy crawl imoti.com`


## Settings

`SKIP_EXISTING` - does not save data if already saved, default `True`

`SEND_EMAIL` - should the application send emails for every new offer, default `False`. Setting it
to `True` requires additional variables to be set as well:

   - `EMAIL_ADDRESS`    - Address of the SMTP server, default `smtp.google.com`
   - `EMAIL_PORT`       - Port on which the SMTP server is running, default `465`
   - `EMAIL_USERNAME`   - User which will send the emails.
   - `EMAIL_PASSWORD`   - Password for the sending user.
   - `EMAIL_RECIPIENTS` - A list of emails which will receive the email notifications.
