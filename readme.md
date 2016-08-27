xkcd-dl
=======

This python3 script downloads images form xkcd.com.

This script is intended to be used in cron jobs to get the newest image file or to download all files.

### Usage

```
usage: xkcd-dl.py [-h] [--all] [--number NUMBER] [--latest] [--saveto SAVETO]
                  [--scan] [-v] [-i]

optional arguments:
  -h, --help       show this help message and exit
  --all            Download all comics.
  --number NUMBER  Download comics number.
  --latest         Download the latest comic.
  --saveto SAVETO  The folder where the comics are to be saved.
  --scan           Scan and index downloaded comics.
  -v, --verbose    Verbose output.
  -i               Ignore errors.
```

### 404 Pages
Configure your webserver to use 404.php for 404 pages.

### License
xkcd comics are licensed under a Creative Commons Attribution-NonCommercial 2.5 License.

I am yet to decide the terms of licensing this code.