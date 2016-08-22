#! /usr/bin/python3

import urllib3
import os.path
#from html.parser import HTMLParser
#from xml.etree.ElementTree import ElementTree
#import xml.etree.ElementTree as ET
from lxml import html

#class xkcdPageParser(HTMLParser):
#      def handle_starttag(self, tag, attrs):
#            # Find div with id 'comic' 
#            if (tag=='div'):
#                  for a in attrs:
#                        if(a[0]=='id'):
#                              if (a[1]=='comic'):
#                                    print ('Found Comic Tag')
                                    

http = urllib3.PoolManager()
xkcdURL='http://xkcd.com/'
r = http.request('GET',xkcdURL+'archive/')
data=r.data.decode("utf-8")
tree = html.fromstring(data,'//xkcd.com')
pages=tree.xpath('//div[@id="middleContainer"]/a/@href')
print(pages)
for p in pages:
      file_number=p.strip('/')
      print(file_number,end=" : ")
      r = http.request('GET',xkcdURL+p)
      data=r.data.decode("utf-8")
      tree = html.fromstring(data,'//xkcd.com')
      comic_image=tree.xpath('//div[@id="comic"]/img/@src')
      comic_caption=tree.xpath('//div[@id="comic"]/img/@title')
      comic_alt=tree.xpath('//div[@id="comic"]/img/@alt')
      print(comic_alt[0]+" : "+comic_caption[0])
      print(comic_image[0],end=" : ")
      comic_file_name=comic_image[0].split('/');
      if (not os.path.isfile('xkcd_archive/'+file_number+'_'+comic_file_name[-1])):
            r = http.request('GET','http:'+comic_image[0])
            f = open('xkcd_archive/'+file_number+'_'+comic_file_name[-1], 'bw')
            f.write(r.data)
            f.close()
            print("ok")
            break
      else:
            print ("File exists!")
