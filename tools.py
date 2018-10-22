import urllib.request
import bs4
import json
import os
import shutil
import youtube_dl
from PIL import Image
import cv2 as cv


def grabFromGoogleImages(search, location='imgs'):
    search = search.replace(' ', '+')

    url = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % search
    safari = {'User-Agent':
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    request = urllib.request.Request(url, headers=safari)
    response = urllib.request.urlopen(request)

    soup = bs4.BeautifulSoup(response.read(), 'lxml')
    imgs = list()

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)

    if os.path.exists(location):
        shutil.rmtree(location)
    os.mkdir(location)
    for i in soup.findAll('div', {"class": "rg_meta"}):
        link, format = json.loads(i.text)["ou"], json.loads(i.text)["ity"]
        imgs.append((link, format))
    for i, (img, format) in enumerate(imgs):
        try:
            if format in ['gif', 'jpg', 'png']:
                x = len(os.listdir(location))+1
                urllib.request.urlretrieve(
                    img, os.path.join(location, '%s.%s' % (x, format)))
                print('downloaded %s from %s' % ('%s.%s' % (x, format), img))
        except Exception as e:
            print('error retrieving image from %s' % img)


def getFaces(img):
    face_cascade = cv.CascadeClassifier(os.path.join(
        'haar_cascade', 'haarcascade_frontalface_default.xml'))
    img = cv.imread(img)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for face in faces:
        face[2] += face[0]
        face[3] += face[1]
    return faces


def cropToFace(loc):
    try:
        img = Image.open(loc)
        faces = getFaces(loc)
        if faces != []:
            img = img.crop()
            img.save(loc)
        else:
            print('no faces found')
    except Exception as e:
        # os.remove(loc)
        print(e)


def cropAll(dir='imgs'):
    for item in os.listdir(dir):
        try:
            if os.path.isfile(os.path.join(dir, item)):
                cropToFace(os.path.join(dir, item))
                print('cropped %s' % item)
        except Exception as e:
            print('error cropping %s, removing it now' % item)
            os.remove(os.path.join(dir, item))


def resizeAll(shape, dir='imgs'):
    for item in os.listdir(dir):
        try:
            img = Image.open(os.path.join(dir, item))
            img = img.resize(shape, Image.ANTIALIAS)
            img.save(os.path.join(dir, item))
            print('resized %s' % item)
        except Exception as e:
            print('error resizing %s, removing it now' % item)
            os.remove(os.path.join(dir, item))


def downloadVideo(url):
    dl = youtube_dl.YoutubeDL()
    dl.extract_info(url)

def framesFromVideo(loc):
    vidcap = cv.VideoCapture('big_buck_bunny_720p_5mb.mp4')
    success,image = vidcap.read()
    count = 0
    while success:
        cv.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1