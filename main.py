import cv2
from detector.detector import PostureDetector
import logging
import time
import pygame
from win10toast import ToastNotifier

def play_alert():
    toaster = ToastNotifier()
    toaster.show_toast("WorkAware", "Corrige tu postura.", duration=5, threaded=True)
    
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/short-bang.mp3")  # asegúrate de que el archivo esté en el mismo directorio
    pygame.mixer.music.play()


cap = cv2.VideoCapture(0)
detector = PostureDetector()

# Configuración del logger
logger = logging.getLogger("PostureLogger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("posture_detector.log", mode='w', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Inicialización de variables
last_posture = None  # 'good' o 'bad'
state_start_time = time.time()

if not cap.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    results = detector.process(frame)
    detector.draw_landmarks(frame, results)

    is_slouched = detector.is_slouched()
    current_posture = 'bad' if is_slouched else 'good'

    # Reproducir sonido si se detecta postura incorrecta
    if current_posture == 'bad':
        time_to_sound = time.time() - state_start_time
        if time_to_sound > 10:  # Reproducir sonido cada 5 segundos
            play_alert()
            # En lugar de o además de play_alert()
            state_start_time = time.time()
    # Detección de cambio de postura
    if current_posture != last_posture and last_posture is not None:
        duration = time.time() - state_start_time
        readable_duration = time.strftime('%H:%M:%S', time.gmtime(duration))
        if last_posture == 'bad':
            logger.info(f"Postura incorrecta durante {readable_duration}")
        else:
            logger.info(f"Postura correcta durante {readable_duration}")
        # Reiniciar el temporizador de estado
        state_start_time = time.time()

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

# Al salir, registrar duración final
final_duration = time.time() - state_start_time
readable_final = time.strftime('%H:%M:%S', time.gmtime(final_duration))
logger.info(f"{'Postura incorrecta' if last_posture == 'bad' else 'Postura correcta'} durante {readable_final}")

cap.release()
cv2.destroyAllWindows()
detector.close()
