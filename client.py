from request_oauthlib import OAuth2Session
from settings import TAGS_TO_IGNORE
import json
import requests
import os 
import webbrowser




class Client:

    def __init__(self, client_key, secret_key):
        self.client_key = client_key
        self.secret_key = secret_key
        self.oauth2_code = ''


    def oauth2_authorize(self):
            oauth = OAuth2Session(self.client_key, redirect_uri='https://freesound.org/home/app_permissions/permission_granted/')

            authorization_url, state = oauth.authorization_url(BASE_URL + AUTHORIZATION)
            webbrowser.open_new(authorization_url)

            authorization_res=input('type in authorization code: ')
            res = request.post(
                BASE_URL + ACCESS_TOKEN,
                params = {
                    'client_id': self.client_key,
                    'client_secret': self.secret_key,
                    'grant_type': 'authorization_code',
                    'code': authorization_res
                }
            )

            access_token = res.json()['access_token']
            self.oauth2_code = access_token
            return True

    def filter_string(self, tags, sr, duration, format, channels):
        return f"filter={self.parse_tags(tags)}{self.parse_duration(duration)}{self.parse_samplerate(sr)}{self.parse_format(format}{self.parse_channels(channels)}"

    
    def parse_tags(self, tags):
        res_string = "" 
        for tag in tags:
            res_string += f"tag:{tag}"
            res_string += "%20"
        #res_string = res_string[:-3]
        return res_string


    def parse_duration(self, from=0, to=15):
        res_string = f"%5B{from}%20TO%20{to}%5D%20" 
        return res_string

    def parse_samplerate(self, rate):
        res_string = ""
        res_string += f"samplerate:{rate}%20"
        return res_string

    def parse_format(self, format):
        res_string = f"type:{format}%20"

    def parse_channels(self, channels):
        res_string = f"channels:{channels}"




    def get_random_sound_data(self, base_url, headers, query='*', fields='id,name,duration,tags'):


        initial_params = {
            'token': self.secret_key,
            'query': query,
            'filter': self.filter_string(),
            'fields': fields,
            'page_size': 15
        }

        res = requests.get(base_url, headers=headers, params=initial_params)
        data = res.json()
        total_results = data['count']

        if total_results == 0:
            return None

        page_size = 15
        max_pages = min(total_results // page_size + 1, 1000)
        attempts = 10

        for _ in range(attempts):  

            random_page = random.randint(1, max_pages)

            current_params = {**initial_params, 'page': random_page}
            res = requests.get(base_url, headers, params=current_params)
            data = res.json()
            results = data.get('results', [])

            valid_sounds = [s for s in results if not set(s.get('tags', [])) & set(TAGS_TO_IGNORE)]



            if valid_sounds:
                random_sound = random.choice(valid_sounds)


                return {
                    'id': random_sound['id'],
                    'name': random_sound['name'],
                    'duration': random_sound['duration'],
                    'description': random_sound['description']
                    'tags': random_sound['tags']
                }

        return None
    
    def download_sample(self, sound_data, target_directory="./"):
        download_headers = {'Authorization': 'Bearer ' + self.oauth2_code}

        url = BASE_URL + SOUNDS + '/' + sound_data['id'] + '/' + DOWNLOAD
        res = requests.get(url, headers=download_headers)

        if res.status_code != 200:
            raise Exception(f"Failed to download sound: {res.status_code} - {res.text}")


        with open(target_directory + sound_data['name'], 'wb') as f:
            f.write(res.content)
            return True



