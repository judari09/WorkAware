# Workaware - Copyright (c) 2025 Juan David Rivaldo Diaz Sierra
# www.linkedin.com/in/juan-david-rivaldo-diaz-sierra-72aa99222 
# Desarrollado por Juan David. Todos los derechos reservados.

# core/session_logger.py
import logging
import time
import matplotlib.pyplot as plt

class SessionLogger:
    def __init__(self, log_file="posture_detector.log"):
        self.logger = logging.getLogger("PostureLogger")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_posture_duration(self, posture, duration):
        readable = time.strftime('%H:%M:%S', time.gmtime(duration))
        self.logger.info(f"Postura {posture} durante {readable}")

    def log_summary(self, good_time, bad_time, total_time):
        self.logger.info(f"Tiempo total de sesión: {time.strftime('%H:%M:%S', time.gmtime(total_time))}")
        self.logger.info(f"Tiempo en postura correcta: {time.strftime('%H:%M:%S', time.gmtime(good_time))}")
        self.logger.info(f"Tiempo en postura incorrecta: {time.strftime('%H:%M:%S', time.gmtime(bad_time))}")

    def plot_summary(self, good_time, bad_time, total_time):
        plt.pie(
            [good_time, bad_time],
            labels=["Postura correcta", "Postura incorrecta"],
            autopct="%1.1f%%",
            startangle=140
        )
        plt.axis('equal')
        plt.title(f"Resumen de la sesión de {time.strftime('%H:%M:%S', time.gmtime(total_time))}")
        plt.show()
