# posture_detector.py
import cv2
import mediapipe as mp



"""_summary_
posture detector es una clase que procesa la imagen de la camra de video 
y detecta si la persona esta encorvada o no.

    Args:
    detection_confidence (float): Confianza mínima para la detección de pose.
    tracking_confidence (float): Confianza mínima para el seguimiento de pose.
    
Returns:
    results (mediapipe.results): Resultados de la detección de pose.
    is_slouched (bool): Indica si la persona está encorvada.
    draw_landmarks (function): Dibuja los puntos de referencia de la pose en el frame.
"""

class PostureDetector:
    def __init__(self, detection_confidence=0.5, tracking_confidence=0.5):
        
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=2,
            smooth_landmarks=True,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.drawing_utils = mp.solutions.drawing_utils
        self.pose_landmarks = None      
        

    def process(self, frame):
        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #procesar frame con mediapipe y retornar resultados 
        # actualizar landmarks de pose
        results = self.holistic.process(rgb)
        self.pose_landmarks = results.pose_landmarks
        return results

    def draw_landmarks(self, frame, results):
        # dibujar puntos de referencia del cuerpo y conexiones
        self.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS)

    def is_slouched(self):
        if not self.pose_landmarks:
            return False

        #obtener puntos de referencia de hombros y boca
        lm = self.pose_landmarks.landmark
        left_shoulder = lm[self.mp_holistic.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = lm[self.mp_holistic.PoseLandmark.RIGHT_SHOULDER]
        left_mouth = lm[self.mp_holistic.PoseLandmark.MOUTH_LEFT]
        right_mouth = lm[self.mp_holistic.PoseLandmark.MOUTH_RIGHT]

        # calcular distancia promedio entre hombros y boca en X
        avg_shoulder_x = (left_shoulder.x + right_shoulder.x) / 2
        avg_mouth_x = (left_mouth.x + right_mouth.x) / 2
        forward_lean = avg_shoulder_x - avg_mouth_x

        # calcular diferencia vertical entre hombros y boca
        avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        avg_mouth_y = (left_mouth.y + right_mouth.y) / 2
        vertical_diff = abs(avg_shoulder_y - avg_mouth_y)
        slouched = forward_lean > 0.05 or vertical_diff < 0.20
        return slouched
    
    def close(self):
        self.holistic.close()
