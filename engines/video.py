import cv2
import face_recognition


class Video:
    def __init__(self, mongo):
        print("Video Engine configured")
        self.mongo = mongo

    def start(self, thread_id, bot_state, is_face_detected):
        print("Video Engine started")
        vid = cv2.VideoCapture(0)
        process_this_frame = True
        while bot_state.value == 1:
            # Grab a single frame of video
            ret, frame = vid.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.existingFaces, face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        # name = known_face_names[first_match_index]

                    # # Or instead, use the known face with the smallest distance to the new face
                    # face_distances = face_recognition.face_distance(self.existingFaces, face_encoding)
                    # best_match_index = np.argmin(face_distances)
                    # if matches[best_match_index]:
                    #     name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame
            #
            # if len(faces) == 0:
            #     is_face_detected.value = 0
            # else:
            #     is_face_detected.value = 1

        vid.release()
        cv2.destroyAllWindows()
