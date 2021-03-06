#! /usr/bin/python3
import argparse
import urllib3
import os.path
import json
import glob
import certifi
from PIL import Image


# Function to print a string iff the -v or --verbose is passed.
# Else, the function dose nothing.
def verbose(string):
    global args
    if args.verbose:
        print(string)


def download_image(config, meta):
    http = config['http']
    args = config['args']
    save_path = args.saveto
    BASE_DIR = config['BASE_DIR']
    comic_file_name = meta['img'].split('/')
    if (not args.noimage):
        if (comic_file_name[-1] != ""):
            if (not os.path.isfile(BASE_DIR + "/" + save_path + '/' + str(meta['num']) + '_' + comic_file_name[-1])):
                r = http.request('GET', meta['img'])
                try:
                    image_file = save_path + '/' + str(meta['num']) + '_' + comic_file_name[-1]
                    f = open(image_file, 'bw')
                    f.write(r.data)
                    f.close()
                except e:
                    print("Error: Cannot create the image file :" + save_path + '/' + file_number + '_' + comic_file_name[-1])
            else:
                verbose("Image file exists. Comic:" + str(meta['num']))
        else:
            print("No comic file to download for "+str(meta['num']))
    return None


def download_meta(config, number):
    xkcdURL = config['xkcdURL']
    args = config['args']
    http = config['http']
    BASE_DIR = config['BASE_DIR']
    save_path = args.saveto
    if (number != -1):
        # if one queries by number
        verbose("Downloading the latest meta")
        cache_file = BASE_DIR + "/" + save_path + "/meta/" + str(number) + "_info.0.json"
    else:
        # If we have chosen --latest or all, always query the internet,
        # since we do not know the number for the latest comic.
        cache_file = BASE_DIR+"/"+save_path+"/meta/NONEXISTANT_info.0.json"
    # check if the info.0.json meta file is cached.
    if (os.path.isfile(cache_file)):
        verbose("Cached meta file found for comic :"+str(number))
        # Meta has already been downloaded - return local file
        try:
            meta_fp = open(save_path + '/meta/' + str(number) + '_info.0.json', 'r')
            meta_json = meta_fp.read()
            meta_fp.close()
        except e:
            print("Error reading cached meta file: " + save_path + '/meta/' + str(number) + '_info.0.json')
            exit()
        meta = json.loads(meta_json)
    else:
        # We will have to download it from the internet - first, build the URL.
        if (number == -1):
            # URL for the latest.
            meta_url = xkcdURL + 'info.0.json'
        else:
            # URL for a numbered comic.
            meta_url = xkcdURL + str(number) + '/info.0.json'
        verbose("Cached meta file not found. Downloading from the internet." + "Comic :" + str(number))
        # download the info.0.json from the built meta_url
        r = http.request('GET', meta_url)
        if (r.status == 200):
            data = r.data.decode("utf-8")
            # Got the data. Now parse it & save it.
            meta = json.loads(data)
            try:
                # save the meta data json.
                meta_fp = open(save_path + "/meta/" + str(meta['num']) + "_info.0.json", 'w')
                meta_fp.write(data)
                meta_fp.close()
            except e:
                # Problem saving - permissions etc.
                print("Error caching meta data to file: " + save_path + "/meta/" + str(meta['num']) + "_info.0.json")
                exit()
        else:
            # Error downloading the meta data from the internet.
            print("Error Downloading meta data from " + meta_url + "\nStatus:"+str(r.status))
            if (not args.i):
                exit()
            meta = {'skip': True}
    # return the meta object
    return meta


def write_meta(config, meta):
    number = meta['num']
    args = config['args']
    BASE_DIR = config['BASE_DIR']
    save_path = args.saveto
    cache_file = BASE_DIR + "/" + save_path + "/meta/" + str(number) + "_info.0.json"
    try:
        # save the meta data json.
        meta_fp = open(cache_file, 'w')
        meta_fp.write(json.dumps(meta))
        meta_fp.close()
    except (RuntimeError, TypeError, NameError):
        # Problem saving - permissions etc.
        print("Error writing meta data to file: " + save_path + "/meta/" + str(meta['num']) + "_info.0.json")
        exit()
    return None


def main(config):
    args = config['args']
    save_path = args.saveto
    # Check if the save_path folder exists and create the folder if it
    # does not exist.
    verbose("Downloading to " + save_path)
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
    elif (args.scan):
        scan(config)
        exit()
    else:
        parser.print_help()
        exit()
    meta = download_meta(config, meta_number)
    if ('skip' in meta):
        verbose("Cannot continue due to errors.")
        exit()
    if (args.latest or args.number):
        # if a single request is made - by number or only latest, download
        # 1 image and we are done.
        verbose("Downloading image now. Comic :"+str(meta['num']))
        download_image(config, meta)
        comic_file_name = meta['img'].split('/')
        image_file = save_path + '/' + str(meta['num']) + '_' + comic_file_name[-1]
        if (comic_file_name[-1] != ""):
            width, height = Image.open(image_file).size
            meta['w'] = width
            meta['h'] = height
            verbose(str(width) + " x " + str(height))
            write_meta(config, meta)
    elif (args.all):
        # if multiple requests are made --all, run in a loop. decrementing the
        # meta['num'] till we reach 1
        while (True):
            download_image(config, meta)
            comic_file_name = meta['img'].split('/')
            image_file = save_path + '/' + str(meta['num']) + '_' + comic_file_name[-1]
            if (comic_file_name[-1] != ""):
                width, height = Image.open(image_file).size
                meta['w'] = width
                meta['h'] = height
                verbose(str(width) + " x " + str(height))
                write_meta(config, meta)
            # So we do not attempt to fetch image 0 - it does not exist.
            next_num = meta['num']
            if (next_num > 1):
                next_num = meta['num'] - 1
                meta = download_meta(config, next_num)
                while ('skip' in meta):
                    next_num = next_num - 1
                    verbose("Skipping to meta :" + str(next_num))
                    meta = download_meta(config, next_num)
            else:
                break
    scan(config)
    return None


def scan(config):
    args = config['args']
    BASE_DIR = config['BASE_DIR']
    save_path = args.saveto
    verbose("Starting metadata scan.")
    # Get a list of all _info.0.json files.
    try:
        meta_file_list = glob.glob(save_path + '/meta/*_info.0.json')
    except e:
        # In case there is an error - permission etc.
        print("Cannot read the meta folder:" + save_path + '/meta/*_info.0.json')
        exit()
    restruct_meta_array = []
    for meta_file in meta_file_list:
        # Open each meta data file & get the meta data
        try:
            fp = open(meta_file, 'r')
            json_string = fp.read()
            meta = json.loads(json_string)
            fp.close()
        except e:
            # Errors like permission etc.
            print("Error reading meta file :" + meta_file + "\nCannot continue.")
            exit()
        # Get the image file part.
        img_url = meta['img'].split('/')
        img_file_name = img_url[-1]
        # Do not add to the indexed metadata if there is no image part and the
        # Image file in not downloaded and only metadata is not enabled.
        if (img_file_name == "" and not args.noimage and not os.path.isfile(BASE_DIR + '/' + save_path + '/' + str(meta['num']) + "_" + img_file_name)):
            verbose(str(meta['num'])+" not found")
            continue
        # Adde selected metadata to the index.
        restruct_meta = {}
        restruct_meta["img"] = save_path + '/' + str(meta['num']) + "_" + img_file_name
        restruct_meta["hot_link"] = meta['img']
        restruct_meta["num"] = meta['num']
        restruct_meta["title"] = meta['title']
        restruct_meta["safe_title"] = meta['safe_title']
        restruct_meta["alt"] = meta['alt']
        restruct_meta["w"] = meta['w']
        restruct_meta["h"] = meta['h']
        # Append and add to metadata.
        restruct_meta_array.append(restruct_meta)
    # Add to the index json file
    complete_meta = json.dumps(restruct_meta_array)
    try:
        fp = open(save_path + '/meta/meta.json', 'w')
        fp.write(complete_meta)
        fp.close()
    except e:
        print("Error creating Metadata file: " + save_path + '/meta/meta.json')
    verbose("Scaning metadata completed")
    return None


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--all", help="Download all comics.", action="store_true")
group.add_argument("--number", help="Download comics number.", type=str)
group.add_argument("--latest", help="Download the latest comic.", action="store_true")
parser.add_argument("--saveto", help="The folder where the comics are to be saved.", type=str, default="xkcd_archive")
parser.add_argument("--scan", help="Scan and index downloaded comics.", action="store_true")
parser.add_argument("--noimage", help="Do not download images. Just metadata.", action="store_true")
parser.add_argument("-v", "--verbose", help="Verbose output.", action="store_true")
parser.add_argument("-i", help="Ignore errors.", action="store_true")
args = parser.parse_args()
config = {}
config['BASE_DIR'] = os.path.dirname(os.path.realpath(__file__))
config['xkcdURL'] = 'http://xkcd.com/'
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
config['http'] = http
config['args'] = args
if args.all:
    verbose("Downloading all comics.")
if __name__ == "__main__":
    main(config)
