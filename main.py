import cv2
from detector.detector import PostureDetector

cap = cv2.VideoCapture(0)
detector = PostureDetector()

# Iniciar la captura de video y procesar los frames
if not cap.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()
    
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Voltear el frame horizontalmente para una visualización más natural
    frame = cv2.flip(frame, 1)
    # Procesar el frame con el detector de postura
    results = detector.process(frame)
    # Dibujar los puntos de referencia de la pose
    detector.draw_landmarks(frame, results)

    if detector.is_slouched():
        cv2.putText(frame, "Corrige tu postura!", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

    cv2.imshow('Posture Monitor', frame)

    if cv2.waitKey(5) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
detector.close()
