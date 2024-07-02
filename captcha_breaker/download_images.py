# import the necessary packages
import argparse
import requests
import time
import os
import cv2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
ap.add_argument("-n", "--num-images", type=int, default=500, help="# of images to download")
args = vars(ap.parse_args())

# initialize the URL that contains the captcha images that we will
# be downloading along with the total number of images downloaded
# thus far
chromedriver_path = '/usr/lib/chromium-browser/chromedriver'
url = "https://www.e-zpassny.com/vector/jcaptcha.do"
total = 0

driver = webdriver.Chrome()
driver.get(url)
# elements = driver.find_elements(By.XPATH, '//*')
# for ele in elements:
#     print('elements in url {}'.format(ele.tag_name))
# loop over the number of images to download
for i in range(0, args["num_images"]):

    img_tag = driver.find_element(By.TAG_NAME, 'script')
    img_url = img_tag.get_attribute('src')
    print(f'Image URL: {img_url}')

    # try to grab a new captcha image
    r = requests.get(img_url, timeout=60)

    if r.status_code == 200:
        # save the image to disk
        p = os.path.sep.join([args["output"], "{}.jpg".format(str(total).zfill(5))])
        f = open(p, "wb")
        f.write(r.content)
        f.close()
        # img = cv2.imread(p)
        # cv2.imshow('image', img)

        # update the counter
        print("[INFO] downloaded: {}".format(p))
        total += 1
    else:
        print('bad response')

    # handle if any exceptions are thrown during the download process
    # except:
    #     print("[INFO] error downloading image...")

    # insert a small sleep to be courteous to the server
    time.sleep(0.1)