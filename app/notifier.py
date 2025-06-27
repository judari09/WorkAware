# Workaware - Copyright (c) 2025 Juan David Rivaldo Diaz Sierra
# www.linkedin.com/in/juan-david-rivaldo-diaz-sierra-72aa99222 
# Desarrollado por Juan David. Todos los derechos reservados.

# core/notifier.py
import pygame
from plyer import notification

class Notifier:
    def __init__(self, sound_path: str):
        """Inicializa el notificador y el reproductor de sonido."""
        self.sound_path = sound_path
        pygame.mixer.init()

    def alert(self, message="Corrige tu postura."):
        """Muestra una notificación y reproduce un sonido de alerta."""
        pygame.mixer.music.stop()  # Detén cualquier sonido anterior
        notification.notify(
            app_icon = "assets/icon.ico", 
            title="WorkAware",
            message=message,
            timeout=0.5
        )
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.music.play()

