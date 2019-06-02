from InstagramPage import *
from FacebookPage import *
from Log import *
import configparser
import time
import re


class Facebook2Instagram:
    def __init__(self):
        self.log = Logger("logs/Facebook2Instagram.log")
        self.log.put("Start")
        self.post_interval = 30 * 60  # check posts every 30 minutes
        self.last_person_pull_time = 0

        configfile_name = "config.ini"
        config = configparser.ConfigParser()
        # Check if there is already a configurtion file
        if not os.path.isfile(configfile_name):
            # Add content to the file
            config.add_section("facebook")
            config.set("facebook", "token", "typehereyourtoken")
            config.set("facebook", "page_id", "typehereyourpageid")
            config.set("facebook", "api_version", "3.3")
            config.add_section("instagram")
            config.set("instagram", "login", "typehereyourusername")
            config.set("instagram", "password", "typehereyourpassword")
            config.set("instagram", "caption", "#nicehashtag")

            with open(configfile_name, 'w') as cfgfile:
                config.write(cfgfile)

        # Load the configuration file
        config.read(configfile_name)
        self.fb = FacebookPage(config["facebook"]["token"], config["facebook"]["page_id"],
                               config["facebook"]["api_version"])
        self.instagram = InstagramPage(config["instagram"]["login"], config["instagram"]["password"],
                                       config["instagram"]["caption"])

    def facebook_to_instagram(self):
        while True:
            post_id, picture_url = self.fb.get_last_post()
            self.log.put("Last Facebook's post -> id:'" + post_id + "', picture_url:'" + picture_url + "'")
            regex = re.compile(
                r"^(?:http|ftp)s?://"  # http:// or https://
                r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
                r"localhost|"  # localhost...
                r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
                r"(?::\d+)?"  # optional port
                r"(?:/?|[/?]\S+)$", re.IGNORECASE)

            if re.match(regex, picture_url) is not None:
                self.instagram.add_post(picture_url)
            time.sleep(self.post_interval)
