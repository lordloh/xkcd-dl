xkcd-dl
=======

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/23950ba7b23a4c4a8e5d0ebc9903a6dc)](https://www.codacy.com/app/lord-loh/xkcd-dl?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=lordloh/xkcd-dl&amp;utm_campaign=Badge_Grade)

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
```bash
python3 xkcd-dl --all -i
```

To hotlink images to xkcd.com, run as -
```bash
python3 xkcd-dl --all -i --noimage
```

Once all the metadata is downloaded, modify the `404.php` file by commenting the line -
```php
define('HOSTED',true);
```

### 404 Pages
Configure your webserver to use 404.php for 404 pages.

#### For apache
1. Clone the repo in an accessable location like /usr/share/apache2/
    
    ```
     sudo git clone https://github.com/lordloh/xkcd-dl.git /mnt/xkcd404
    ```
    
    Change ownership or permissions of  the `timefile`. The `timefile` ensures that only one comic is chosen and displayed for 15 minutes. This discourages people from pressing `F5` on your 404 pages for entertainment.
    
    ```
    sudo chown www-data:www-data timefile
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

    ```bash
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
