from requests_oauthlib import OAuth2Session
from settings import TAGS_TO_IGNORE, BASE_URL, ACCESS_TOKEN, AUTHORIZE, SOUNDS, DOWNLOAD, PACKS
import json
import requests
import os 
import webbrowser
from pathlib import Path
from requests.exceptions import ChunkedEncodingError, ConnectionError
from http.client import IncompleteRead
from multiprocessing import Process


class Client:

    def __init__(self, client_key, secret_key):
        self.client_key = client_key
        self.secret_key = secret_key
        self.redirect_uri = "http://localhost:5000/callback"
        self.oauth2_code = None


    def oauth2_authorize(self):
        auth_url = f"https://freesound.org/apiv2/oauth2/authorize/?client_id={self.client_key}&response_type=code&redirect_uri={self.redirect_uri}"
        webbrowser.open_new(auth_url)


    def fetch_access_token(self, code):
        TOKEN_URL = "https://freesound.org/apiv2/oauth2/access_token/"

        data = {
            "client_id": self.client_key,
            "client_secret": self.secret_key,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }

        res = requests.post(TOKEN_URL, data=data)
        res.raise_for_status()

        token_data = res.json()
        self.oauth2_code = token_data["access_token"]
        return token_data


    def aoauth2_authorize(self):
            oauth = OAuth2Session(self.client_key, redirect_uri='https://freesound.org/home/app_permissions/permission_granted/')

            authorization_url, state = oauth.authorization_url(BASE_URL + AUTHORIZE)
            webbrowser.open_new(authorization_url)

            authorization_res=input('type in authorization code: ')
            res = requests.post(
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
        return f"filter={self.parse_tags(tags)}{self.parse_duration(duration)}{self.parse_samplerate(sr)}{self.parse_format(format)}{self.parse_channels(channels)}"

    
    def parse_tags(self, tags):
        res_string = "" 
        for tag in tags:
            res_string += f"tag:{tag}"
            res_string += "%20"
        return res_string


    def parse_duration(self, duration):
        res_string = f"%5B{duration[0]}%20TO%20{duration[1]}%5D%20" 
        return res_string

    def parse_samplerate(self, rate):
        res_string = ""
        res_string += f"samplerate:{rate}%20"
        return res_string

    def parse_format(self, format):
        res_string = f"type:{format}%20"
        return res_string

    def parse_channels(self, channels):
        res_string = f"channels:{channels}"
        return res_string

    def get_packsounds(self, pack_id, page_size):
        headers = {
            'Authorization': f'Token {self.secret_key}'
        }
        params = {
            'fields': 'id,name',
            'page_size': page_size
        }

        url = f"{BASE_URL}{PACKS}{pack_id}/{SOUNDS}"
        res = requests.get(url, params=params, headers=headers)
        data = res.json()
        sounds = [{'id': sound['id'], 'name': sound['name']} for sound in data.get('results')]
        return sounds




    def get_random_sound_data(self, base_url, headers, query='*', fields='id,name,duration,tags', page_size=15):


        initial_params = {
            'token': self.secret_key,
            'query': query,
            'filter': self.filter_string(),
            'fields': fields,
            'page_size': page_size
        }

        res = requests.get(base_url, headers=headers, params=initial_params)
        data = res.json()
        total_results = data['count']

        if total_results == 0:
            return None

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
                    'description': random_sound['description'],
                    'tags': random_sound['tags']
                }

        return None
    
    def download_samples(self, samples, target_directory="./", retries=5, chunk_size=8192):
        download_headers = {'Authorization': f'Bearer {self.oauth2_code}'}
        print(self.oauth2_code)
        Path(target_directory).mkdir(parents=True, exist_ok=True)

        for sample in samples:

            attempt = 1
            url = f'{BASE_URL}{SOUNDS}{sample['id']}/{DOWNLOAD}'
            while attempt <= retries:
                try:
                    with requests.get(url, headers=download_headers, stream=True, timeout=30) as r:

                        
                        output_file = Path(target_directory + '/' + sample['name'])


                        with open(output_file, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=chunk_size):
                                if (chunk):
                                    f.write(chunk)
                            print(f"Downloaded {sample['name']} to target directory {target_directory}")
                            break
                except (ChunkedEncodingError, ConnectionError, IncompleteRead) as e:
                    print(f"Download Error, attempt {attempt}/{retries}: {e}")
                    attempt += 1
                    time.sleep(1)
                    print("Failed moving to next sample")

    def multi_process_download_samples(self, samples, processes=1, target_directory="./"):
        it = iter(samples)
        samples_list = [samples[i:i+processes] for i in range(0, len(samples), processes)]
        process_list = [Process(target=self.download_samples, args=(sample_list, target_directory)) for sample_list in samples_list]

        for process in process_list:
            process.start()

        for process in process_list:
                    process.join()
