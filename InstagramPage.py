from Log import *
from InstagramAPI import InstagramAPI
import urllib3
from PIL import Image


def download_web_image(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    with open("picture_orig.jpg", 'wb') as out:
        while True:
            data = r.read(65536)
            if not data:
                break
            out.write(data)

    r.release_conn()


def make_square(img, min_size=256, fill_color=(255, 255, 255)):
    x, y = img.size
    size = max(min_size, x, y)
    new_img = Image.new('RGB', (size, size), fill_color)
    new_img.paste(img, (int((size - x) / 2), int((size - y) / 2)))
    return new_img


class InstagramPage:
    def __init__(self, login, password, caption):
        self.log = Logger("logs/InstagramPage.log")
        self.caption = caption
        self.instagram_api = InstagramAPI(login, password)
        self.instagram_api.login()
        if self.instagram_api.isLoggedIn:
            self.log.put("Logged in as " + login + ".")
        else:
            self.log.put("Login failed for " + login + ".")
            exit(1)

    def add_post(self, picture_url):
        try:
            download_web_image(picture_url)
            pic = make_square(Image.open("picture_orig.jpg"))
            pic.save("picture.jpg")

            # It uses everytime the same caption, I don't need to copy from fb for my purpose lmao
            if not self.instagram_api.isLoggedIn:
                self.instagram_api.login()

            if self.instagram_api.isLoggedIn:
                self.instagram_api.uploadPhoto("picture.jpg", caption=self.caption)
                self.log.put("Uploaded.")
            else:
                self.log.put("Can't upload: " + picture_url)

            os.remove("picture_orig.jpg")
            os.remove("picture.jpg")
        except FileNotFoundError:
            self.log.put("File non esistente.")
        except Exception as e:
            self.log.put("Errore: " + str(e))
