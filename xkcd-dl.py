#! /usr/bin/python3
import argparse
import urllib3
import os.path
import json


# Function to print a string iff the -v or --verbose is passed.
# Else, the function dose nothing.
def verbose(string):
    global args
    if args.verbose:
        print(string)


def download_image(meta):
    global http
    comic_file_name = meta['img'].split('/')
    if (not os.path.isfile(save_path + '/' +
                        str(meta['num']) + '_' + comic_file_name[-1])):
        r = http.request('GET', meta['img'])
        try:
            f = open(save_path + '/' +
                     str(meta['num']) + '_' + comic_file_name[-1], 'bw')
            f.write(r.data)
            f.close()
        except e:
            print("Error: Cannot create the image file :" +
                  save_path + '/' + file_number + '_' + comic_file_name[-1])
    else:
        print("File exists!")


def download_meta(number):
    global xkcdURL, save_path, http, BASE_DIR
    if (number != -1):
        # if one queries by number
        cache_file = BASE_DIR + "/" + save_path + "/meta/" \
                     + str(number) + "_info.0.json"
    else:
        # If we have chosen --latest or all, always query the internet,
        # since we do not know the number for the latest comic.
        cache_file = BASE_DIR+"/"+save_path+"/meta/NONEXISTANT_info.0.json"
    # check if the info.0.json meta file is cached.
    if (os.path.isfile(save_path + '/meta/' + str(number) + '_info.0.json')):
        verbose("Cached meta file found!")
        # Meta has already been downloaded - return local file
        try:
            meta_fp = open(save_path + '/meta/' +
                           str(number) + '_info.0.json', 'r')
            meta_json = meta_fp.read()
            meta_fp.close()
        except:
            print("Error reading cached meta file: " + save_path +
                  '/meta/' + str(number) + '_info.0.json')
            exit()
        meta = json.loads(meta_json)
    else:
        # We will have to download it from the internet - first, build the URL.
        verbose("Cached meta file not found. Downloading from the internet")
        if (number == -1):
            # URL for the latest.
            meta_url = xkcdURL + 'info.0.json'
        else:
            # URL for a numbered comic.
            meta_url = xkcdURL + str(number) + '/info.0.json'
        # download the info.0.json from the built meta_url
        r = http.request('GET', meta_url)
        if (r.status == 200):
            data = r.data.decode("utf-8")
            # Got the data. Now parse it & save it.
            meta = json.loads(data)
            try:
                # save the meta data json.
                meta_fp = open(save_path + "/meta/" +
                               str(meta['num']) + "_info.0.json", 'w')
                meta_fp.write(data)
                meta_fp.close()
            except:
                # Problem saving - permissions etc.
                print("Error caching meta data to file: " + save_path +
                      "/meta/" + str(meta['num']) + "_info.0.json")
                exit()
        else:
            # Error downloading the meta data from the internet.
            print("Error Downloading meta data from " + meta_url +
                  "\nStatus:"+str(r.status))
            exit()
    # return the meta object
    return meta


def main():
    global args, save_path
    http = urllib3.PoolManager()
    # Check if the save_path folder exists and create the folder if it
    # does not exist.
    if (not os.path.isdir(save_path)):
        verbose("Folder " + save_path + " does not exist. Creating it.")
        try:
            os.mkdir(save_path)
            os.mkdir(save_path + '/meta')
        except e:
            print("Error: Cannot create the folder " + save_path)
            exit()
    if (args.all or args.latest):
        # if --all or --latest is passed, get meta from the internet.
        meta_number = -1
    elif (args.number):
        # Else get meta by number.
        meta_number = args.number
    meta = download_meta(meta_number)
    if (args.latest or args.number):
        # if a single request is made - by number or only latest, download
        # 1 image and we are done.
        verbose("Downloading image now.")
        download_image(meta)
    elif (args.all):
        # if multiple requests are made --all, run in a loop. decrementing the
        # meta['num'] till we reach 1
        while (meta['num'] >= 1):
            download_image(meta)
            # So we do not attempt to fetch image 0 - it does not exist.
            if (meta['num'] > 1):
                meta = download_meta(meta['num']-1)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--all", help="Download all comics.", action="store_true")
group.add_argument("--number", help="Download comics number.", type=str)
group.add_argument("--latest", help="Download the latest comic.",
                   action="store_true")
parser.add_argument("--saveto",
                    help="The folder where the comics are to be saved.",
                    type=str, default="xkcd_archive")
parser.add_argument("-v", "--verbose", help="Verbose output.",
                    action="store_true")
args = parser.parse_args()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
xkcdURL = 'http://xkcd.com/'
http = urllib3.PoolManager()
if args.all:
    verbose("Downiloading all comics.")
save_path = args.saveto
verbose("Downloading to "+save_path)
if __name__ == "__main__":
    main()
