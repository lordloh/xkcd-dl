xkcd-dl
=======

This python3 script downloads images form xkcd.com.

This script is intended to be used in cron jobs to get the newest image file or to download all files.

### Usage


```
usage: xkcd-dl.py [-h] [--all | --number NUMBER | --latest] [--saveto SAVETO]
                  [--scan] [--noimage] [-v] [-i]

optional arguments:
  -h, --help       show this help message and exit
  --all            Download all comics.
  --number NUMBER  Download comics number.
  --latest         Download the latest comic.
  --saveto SAVETO  The folder where the comics are to be saved.
  --scan           Scan and index downloaded comics.
  --noimage        Do not download images. Just metadata.
  -v, --verbose    Verbose output.
  -i               Ignore errors.
```

To host images yourself, run as -
```
python3 xkcd-dl --all -i
```

To hotlink images to xkcd.com, run as -
```
python3 xkcd-dl --all -i --noimage
```


### 404 Pages
Configure your webserver to use 404.php for 404 pages. The `404.hot.php` hotlinks images to xkcd.com instead of hosting it yourself.

#### For apache
1. Clone the repo in an accessable location like /usr/share/apache2/
    
    ```
     sudo git clone https://github.com/lordloh/xkcd-dl.git /mnt/xkcd404
    ```

2. Create a directory alias for apache

    In the file `/etc/apache2/mods-avaliable/alias.conf`
    
    ```
        Alias /error/ "/mnt/xkcd404/"

        <Directory "/mnt/xkcd404">
                Options FollowSymlinks
                AllowOverride None
                Require all granted
        </Directory>
    ```
    
3. Enable the module if it is not already enabled

    ```
    sudo a2enmod alias
    ```

4. Set the error pages using the directive -
    
    ```
    ErrorDocument 404 /error/404.php
    ```
    
    This may be done in appropriate file like the virtual host file etc. For global xkcd error pages put this line in `/etc/apache2/conf-enabled/localized-error-pages.conf`

### License
xkcd comics are licensed under a Creative Commons Attribution-NonCommercial 2.5 License.

I am yet to decide the terms of licensing this code.