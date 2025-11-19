import numpy as np
from settings import *



class DataProcessor:
    
    def __init__(self):
        self.data_array = np.empty([])

    def process_tags(self, tags):

        processed_tags = []

        for tag in tags:
            tag = tag.lower()
            tag = tag.replace('-', ' ')
            if not tag in TAGS_TO_IGNORE and not tag.isdigit():
                processed_tag.append(tag)

        return processed_tags

    def size(self):
        return self.data_array.shape[0]

    def process_samples(self, sounds):
        if sounds == null or sounds == {}:
            raise Exception('No Sounds to Process into csv')


        for idx, sound in enumerate(sounds):

    def save_to_csv(self, file_name):
        file = file_name + '.csv'
        np.savetxt(file, self.data_array, delimiter=',', fmt='%s')

    def data_parse(self, results):
        if results is {} or results is None:
            return {}
