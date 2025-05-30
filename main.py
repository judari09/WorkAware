import cv2
from detector.detector import PostureDetector
import logging
import time
import pygame
from win10toast import ToastNotifier
import matplotlib.pyplot as plt


cap = cv2.VideoCapture(0)
detector = PostureDetector()

# Logger setup
logger = logging.getLogger("PostureLogger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("posture_detector.log", mode='w', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Timing variables
last_posture = None
sesion_start_time = time.time()
posture_start_time = time.time()
last_alert_time = None
alert_interval = 10  # segundos entre alertas de mala postura
time_sesion = None
good_posture_time = 0
bad_posture_time = 0


def play_alert():
    toaster = ToastNotifier()
    toaster.show_toast("WorkAware", "Corrige tu postura.", duration=5, threaded=True)
    
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/short-bang.mp3")
    pygame.mixer.music.play()

def log_session_summary():
    finish_time = time.time()
    total_time = finish_time - sesion_start_time
    
    labels = ['postura correcta', 'postura incorrecta']
    data_sesion = [good_posture_time, bad_posture_time]
    plt.pie(data_sesion, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f'Resumen de la sesión de {time.strftime("%H:%M:%S", time.gmtime(total_time))}')
    plt.show()
    logger.info(f"Tiempo total de sesión: {time.strftime('%H:%M:%S', time.gmtime(total_time))}")
    logger.info(f"Tiempo en postura correcta: {time.strftime('%H:%M:%S', time.gmtime(good_posture_time))}")
    logger.info(f"Tiempo en postura incorrecta: {time.strftime('%H:%M:%S', time.gmtime(bad_posture_time))}")


try:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        results = detector.process(frame)
        detector.draw_landmarks(frame, results)

        is_slouched = detector.is_slouched()
        current_posture = 'bad' if is_slouched else 'good'
        current_time = time.time()

        # Emitir alerta si se mantiene la mala postura
        if current_posture == 'bad':
            if last_alert_time is None or (current_time - last_alert_time) >= alert_interval:
                play_alert()
                last_alert_time = current_time

        # Cambio de postura: registrar en log
        if current_posture != last_posture and last_posture is not None:
            duration = current_time - posture_start_time
            readable_duration = time.strftime('%H:%M:%S', time.gmtime(duration))
            if last_posture == 'bad':
                bad_posture_time += duration
                logger.info(f"Postura incorrecta durante {readable_duration}")
            else:
                good_posture_time += duration
                logger.info(f"Postura correcta durante {readable_duration}")
            posture_start_time = current_time
            last_alert_time = None  # reiniciar alertas si mejora la postura

        # Visual feedback
        if is_slouched:
            cv2.putText(frame, "Corrige tu postura!", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Postura correcta", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 200, 0), 2)

        last_posture = current_posture
        cv2.imshow('Posture Monitor', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break
except Exception as e:
    logger.error(f"Error durante la sesión: {e}")

finally:
    # Agregar el último tramo activo antes de cerrar
    end_time = time.time()
    last_duration = end_time - posture_start_time
    if last_posture == 'bad':
        bad_posture_time += last_duration
    elif last_posture == 'good':
        good_posture_time += last_duration
        
    log_session_summary()
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
