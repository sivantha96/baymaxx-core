import time
import numpy as np
import cv2
import face_recognition
from threading import Thread


class Video:
    def __init__(self, mongo):
        print("Video Engine configured")
        self.mongo = mongo

    def get_current_user(self):
        current_face = self.mongo.db.faces.find_one({"name": "current_face"})
        if current_face is None:
            return 'unknown'
        if current_face['encoding'] is None:
            return 'unknown'
        saved_faces = self.mongo.db.saved_faces.find()
        saved_faces_encodings = []
        for face in saved_faces:
            saved_faces_encodings.append(np.fromiter(face['encoding'], dtype=float))
        match = face_recognition.compare_faces(saved_faces_encodings,
                                               np.fromiter(current_face['encoding'], dtype=float))

        if match[0]:
            return 'sivantha'
        else:
            return 'unknown'

    # def start_checking_for_changes(self):
    #     while True:
    #         time.sleep(2)
    #         recognized_face = self.mongo.db.faces.find_one({"name": "recognized_face"})
    #         current_face = self.mongo.db.faces.find_one({"name": "current_face"})
    #         if recognized_face is None:
    #             if current_face is not None:
    #                 self.mongo.db.faces.update_one({"name": 'recognized_face'},
    #                                                {"$set": {"encoding": current_face['encoding']}},
    #                                                True)
    #         else:
    #             matches = face_recognition.compare_faces([np.fromiter(recognized_face['encoding'], dtype=float)], np.fromiter(current_face['encoding'], dtype=float))
    #             print(matches[0] == True)
    #
    #
    #         print(current_face)

    def start_scanning_faces(self):
        vid = cv2.VideoCapture(0)
        process_this_frame = True
        current_encoding = None
        while True:
            # Grab a single frame of video
            ret, frame = vid.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            if len(face_encodings) > 0:
                self.mongo.db.faces.update_one({"name": 'current_face'},
                                               {"$set": {"encoding": face_encodings[0].tolist()}},
                                               True)
            else:
                self.mongo.db.faces.update_one({"name": 'current_face'},
                                               {"$set": {"encoding": None}},
                                               True)
            # if face_encoding is None:
            #     current_encoding = face_encoding
            # else:
            #
            #     matches = face_recognition.compare_faces([current_encoding], face_encoding)
            # face_names = []
            # # See if the face is a match for the known face(s)
            #
            # name = "Unknown"
            #
            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     # name = known_face_names[first_match_index]
            #
            # # # Or instead, use the known face with the smallest distance to the new face
            # # face_distances = face_recognition.face_distance(self.existingFaces, face_encoding)
            # # best_match_index = np.argmin(face_distances)
            # # if matches[best_match_index]:
            # #     name = known_face_names[best_match_index]
            #
            # face_names.append(name)

            time.sleep(1)

        vid.release()
        cv2.destroyAllWindows()

    def start(self):
        print("Video Engine started")
        # face_check = Thread(target=self.start_checking_for_changes)
        face_scan = Thread(target=self.start_scanning_faces)

        # face_check.start()
        face_scan.start()

        # face_check.join()
        face_scan.join()
