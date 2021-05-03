import pymongo


class VideoService:
    def __init__(self):
        print("Video service configured")
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["baymaxx"]

    def compare_faces(self):
        col = self.db["faces"]
        faces = col.find()
