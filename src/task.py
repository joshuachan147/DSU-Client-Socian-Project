import cv2
import json
from google.cloud import vision

class TrackingTask:
    def __init__(self, video_loc, description):
        self.video = cv2.VideoCapture(video_loc)
        self.description = description

        with open('data/clothing_categories.json') as f:
            self.categorizer = json.load(f)

        self.vision_client = vision.ImageAnnotatorClient.from_service_account_file(
            'service_account.json')

    def object_priority(self, obj):
        if obj.name == 'person':
            return 0
        elif obj.name in self.categorizer:
            return 1
        else:
            return 2