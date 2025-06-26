# core/notifier.py
import pygame
from win10toast import ToastNotifier
""" _summary_
    Clase para manejar las notificaciones y alertas de sonido.
    Esta clase utiliza win10toast para mostrar notificaciones en Windows
"""
class Notifier:
    def __init__(self, sound_path: str):
        """Inicializa el notificador y el reproductor de sonido."""
        self.toaster = ToastNotifier()
        self.sound_path = sound_path
        pygame.mixer.init()

    def alert(self, message="Corrige tu postura."):
        """Muestra una notificación y reproduce un sonido de alerta."""
        self.toaster.show_toast("WorkAware", message, duration=5, threaded=True)
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.music.play()
