import cv2
import face_recognition
import time

class OnlineClassMonitor:
    def __init__(self, class_duration_seconds=3600):  # Default class duration: 1 hour
        self.class_duration = class_duration_seconds
        self.start_time = time.time()
        self.in_class = False
        self.total_time_in_class = 0
        self.total_time_away = 0
        self.last_face_time = None

    def detect_faces(self, frame):
        face_locations = face_recognition.face_locations(frame)
        return len(face_locations) > 0

    def process_frame(self, frame):
        # Face detection
        face_detected = self.detect_faces(frame)

        # Update timestamps based on face detection
        if face_detected:
            if not self.in_class:
                self.in_class = True
                self.last_face_time = time.time()
        else:
            if self.in_class:
                self.in_class = False
                time_away = time.time() - self.last_face_time
                self.total_time_away += time_away
                print(f"Away from camera for {time_away:.2f} seconds")

    def run_monitor(self):
        # Open webcam
        cap = cv2.VideoCapture(0)

        while time.time() - self.start_time < self.class_duration:
            ret, frame = cap.read()

            # Process the frame for face detection
            self.process_frame(frame)

            # Display the resulting frame
            cv2.imshow('Webcam', frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Calculate total time in class and class duration
        self.total_time_in_class = time.time() - self.start_time - self.total_time_away

        # Print total times
        print(f"Total time in class: {self.total_time_in_class:.2f} seconds")
        print(f"Total time away from class: {self.total_time_away:.2f} seconds")
        print(f"Total class duration: {self.class_duration:.2f} seconds")

        # Release the webcam and close windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create an instance of OnlineClassMonitor
    monitor = OnlineClassMonitor(class_duration_seconds=1800)  # Set class duration: 30 minutes

    # Run the monitoring system
    monitor.run_monitor()