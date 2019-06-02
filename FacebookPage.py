from Log import *
import requests


class FacebookPage:
    def __init__(self, token, page_id, api_version):
        self.log = Logger("logs/FacebookPage.log")
        self.token = token
        self.page_id = page_id
        self.api_version = api_version
        self.last_post_id_file = "last_post_id"
        self.errorcount = 0

    def get_last_post(self):
        post_id = ""
        picture_url = ""
        params = {"fields": "full_picture", "limit": "1", "access_token": self.token}
        graph_api = "https://graph.facebook.com/v" + self.api_version + "/" + self.page_id + "/posts"
        response = None
        try:
            response = requests.get(graph_api, params=params)
            time.sleep(5)
            if str(response) != "<Response [200]>":
                self.log.put(str(response) + ": " + response.text)
                self.errorcount += 1
                if self.errorcount > 10:
                    exit(1)
                return post_id, picture_url
            else:
                self.errorcount = 0
        except Exception as e:
            self.log.put("Error at request get: " + str(e))
            try:
                self.log.put(response.text)
            except Exception:
                self.log.put("Response is None.")
            return post_id, picture_url

        if not os.path.isfile(self.last_post_id_file):
            # Create the configuration file as it doesn't exist yet
            lastpostfile = open(self.last_post_id_file, 'w')
            lastpostfile.close()

        with open(self.last_post_id_file) as f:
            last_post_id = f.read()

        json_response = response.json()
        post = json_response['data'][0]

        if last_post_id != post["id"]:
            post_id = post["id"]
            picture_url = post["full_picture"]
            lastpostfile = open(self.last_post_id_file, 'w')
            lastpostfile.write(post_id)
            lastpostfile.close()

        self.log.put("Request done.")
        return post_id, picture_url
