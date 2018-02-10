import requests
from urllib.request import urlretrieve
import json
from selenium import webdriver
import sys
from slugify import slugify


def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


def main():
	#edit this part
	folder = "C:\\Users\\trihard\\some\\location\\" # dont forget last double slash


	
	driver = webdriver.PhantomJS()
	with open('ice.json') as data_file:    
	    links = json.load(data_file)

	count = 0 # to help with duplicates
	for link in links:
		count += 1
		driver.get(link)

		# video link
		vidLink = driver.find_element_by_xpath('//meta[@property="og:image:secure_url"]').get_attribute("content")

		# video name
		name = slugify(driver.find_element_by_xpath('//meta[@property="og:title"]').get_attribute('content'))
		vidLink = (vidLink.replace('.shot.thumb.jpg','.shot.mp4')).replace("thumbs","capture")
		location = folder + name + ".mp4"

		# check if file exists, if so add count to end of filename
		my_file = Path(location)
		if my_file.is_file():
			print("{} exists!".format(location))
			location = folder + name + str(count) + ".mp4"
			print("Downloading {}".format(vidLink))
			urlretrieve(vidLink, location, reporthook)
			print('DONE!')
		else:
			print("Downloading {}".format(vidLink))
			urlretrieve(vidLink, location, reporthook)
			print('DONE!')
	driver.quit()

if __name__ == '__main__':
	main()
