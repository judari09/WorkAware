# core/posture_monitor.py
import time
import cv2
from detector.detector import PostureDetector
from app.notifier import Notifier
from app.session_logger import SessionLogger

class PostureMonitor:
    def __init__(self):
        self.detector = PostureDetector()
        self.notifier = Notifier("sounds/short-bang.mp3")
        self.logger = SessionLogger()
        self.cap = cv2.VideoCapture(0)
        self.running = False  # Flag para controlar el hilo
        self.good_time = 0
        self.bad_time = 0
        self.start_time = time.time()
        self.posture_start_time = time.time()
        self.last_alert_time = None
        self.alert_interval = 10
        self.last_posture = None

    def run(self):
        self.running = True
        try:
            while self.cap.isOpened() and self.running:
                ret, frame = self.cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                results = self.detector.process(frame)
                #self.detector.draw_landmarks(frame, results)

                slouched = self.detector.is_slouched()
                posture = "bad" if slouched else "good"
                now = time.time()

                # Alert if slouching continuously
                if posture == "bad" and (self.last_alert_time is None or now - self.last_alert_time >= self.alert_interval):
                    self.notifier.alert()
                    self.last_alert_time = now

                # Cambio de postura
                if posture != self.last_posture and self.last_posture is not None:
                    duration = now - self.posture_start_time
                    self.logger.log_posture_duration(self.last_posture, duration)
                    if self.last_posture == "bad":
                        self.bad_time += duration
                    else:
                        self.good_time += duration
                    self.posture_start_time = now
                    self.last_alert_time = None

                # Mostrar estado
                msg = "Corrige tu postura!" if slouched else "Postura correcta"
                color = (0, 0, 255) if slouched else (0, 200, 0)
                cv2.putText(frame, msg, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
                cv2.imshow("Posture Monitor", frame)

                self.last_posture = posture

                if cv2.waitKey(5) & 0xFF == 27:
                    break
        finally:
            self._terminate()

    def stop(self):
        self.running = False

    def _terminate(self):
        # registrar último tramo
        end = time.time()
        last_duration = end - self.posture_start_time
        if self.last_posture == "bad":
            self.bad_time += last_duration
        elif self.last_posture == "good":
            self.good_time += last_duration

        total = end - self.start_time
        self.logger.log_summary(self.good_time, self.bad_time, total)
        #self.logger.plot_summary(self.good_time, self.bad_time, total)

        self.cap.release()
        cv2.destroyAllWindows()
        self.detector.close()
