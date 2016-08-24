#! /usr/bin/python3
import argparse
import urllib3
import os.path
from lxml import html

def verbose(string):
      global args
      if args.verbose:
            print(string)

def main():
      global args, save_path
      http = urllib3.PoolManager()
      xkcdURL='http://xkcd.com/'
      # Check and create a floder to save images to.
      if (not os.path.isdir(save_path)):
            verbose("Folder "+save_path+" does not exist. Creating it.")
            os.mkdir(save_path)
      # Download all
      if (args.all or args.latest):
            # Download the index of comics.
            r = http.request('GET',xkcdURL+'archive/')
            if (r.status==200):
                  data=r.data.decode("utf-8")
                  tree = html.fromstring(data,'//xkcd.com')
                  pages=tree.xpath('//div[@id="middleContainer"]/a/@href')
            else:
                  verbose("Status:"+str(r.status))
                  pages=[]
      elif (args.number):
            # If a comic number is specified, download that.
            pages=[args.number]
      
      # Download the latest comic.
      if (args.latest):
            pages=[pages[0]]
            verbose("Downloading the latest comic.")
      #verbose(pages)
            
      for p in pages:
            file_number=p.strip('/')
            print(file_number,end=" : ")
            r = http.request('GET',xkcdURL+p)
            if (r.status==200):
                  data=r.data.decode("utf-8")
                  tree = html.fromstring(data,'//xkcd.com')
                  comic_image=tree.xpath('//div[@id="comic"]//img/@src')
                  comic_caption=tree.xpath('//div[@id="comic"]//img/@title')
                  comic_alt=tree.xpath('//div[@id="comic"]//img/@alt')
                  #print(comic_alt[0]+" : "+comic_caption[0])
                  #print(comic_image[0],end=" : ")
                  comic_file_name=comic_image[0].split('/');
                  if (not os.path.isfile(save_path+'/'+file_number+'_'+comic_file_name[-1])):
                        r = http.request('GET','http:'+comic_image[0])
                        f = open(save_path+'/'+file_number+'_'+comic_file_name[-1], 'bw')
                        f.write(r.data)
                        f.close()
                        #print("ok")
                        break
                  else:
                        print ("File exists!")
            elif (r.status==404):
                  verbose("Error 404: File not found.")
            else:
                  verbose("Status:"+str(r.status))

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--all", help="Download all comics.", action="store_true")
group.add_argument("--number", help="Download comics number.",type=str)
group.add_argument("--latest", help="Download the latest comic.", action="store_true")
parser.add_argument("--saveto",help="The folder where the comics are to be saved.",type=str,default="xkcd_archive")
parser.add_argument("-v","--verbose", help="Verbose output", action="store_true")
args = parser.parse_args()

if args.all:
      verbose("Downiloading all comics.")
save_path=args.saveto
verbose("Downloading to "+save_path)
if __name__ == "__main__": main()