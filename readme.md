xkcd-dl
=======

This python3 script downloads images form xkcd.com.

This script is intended to be used in cron jobs to get the newest image file or to download all files.

This project is inspired by some 404 pages that had xkcd comics.

### Usage

`xkcd-dl.py [-h] [--all | --number NUMBER | --latest] [--saveto SAVETO] [-v]`

optional arguments:
  -h, --help       show this help message and exit
  --all            Download all comics.
  --number NUMBER  Download comics number.
  --latest         Download the latest comic.
  --saveto SAVETO  The folder where the comics are to be saved.
  -v, --verbose    Verbose output.

### License
xkcd comics are licensed under a Creative Commons Attribution-NonCommercial 2.5 License.

I am yet to decide the terms of licensing this code.