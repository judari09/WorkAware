# WorkAware 🧠💺

**WorkAware** es una estación personal de productividad y salud digital. Ayuda al usuario a mantener una postura adecuada frente al computador, emite alertas correctivas, registra estadísticas de postura durante la sesión y genera reportes gráficos.

---

## 📌 Funcionalidades actuales

✅ **Monitoreo de postura en tiempo real**  
Detecta si el usuario está encorvado usando visión por computadora.

✅ **Alertas correctivas**  
Si se mantiene una mala postura durante más de 10 segundos, se emite una alerta sonora y una notificación de sistema.

✅ **Registro de actividad**  
Guarda un log con:
- Cambios de postura detectados.
- Tiempos acumulados de buena y mala postura.
- Tiempo total de la sesión.

✅ **Reporte gráfico**  
Al finalizar la sesión, se genera un gráfico de pastel que resume el tiempo dedicado a cada tipo de postura.

---

## ⚙️ Instalación

### 🔄 Requisitos previos

- Python 3.10 o superior
- Sistema operativo: Windows 10 o superior (por el uso de notificaciones `win10toast`)
- Webcam funcional

### 🧪 Usando `uv` (recomendado)

1. Instala `uv` (si aún no lo tienes):

   ```
   curl -Ls https://astral.sh/uv/install.sh | sh
   ```
2. Clona el repositorio:
    ```
    git clone https://github.com/tuusuario/workaware.git
    cd workaware
    ```

3. Instala las dependencias:

    ```
    uv pip install -r requirements.txt
    ```
4. Ejecuta la aplicación:
    ```
    uv venv exec python main.py
    ```
5. 📁 Estructura del proyecto
    ```
    workaware/
    │
    ├── main.py                     # Ejecución principal
    ├── detector/
    │   └── detector.py             # Detección de postura (MediaPipe)
    ├── sounds/
    │   └── short-bang.mp3          # Sonido de alerta
    ├── posture_detector.log        # Log generado por sesión
    ├── requirements.txt            # Dependencias del proyecto
    └── README.md                   # Este archivo
    ```
6. 🚀 Próximas funcionalidades

    🔜 Gestión de tareas
    Permite ingresar tareas y obtener una organización óptima de ejecución, basada en prioridades.

    🔜 Sugerencias de descansos inteligentes
    Basado en tiempos de productividad y mala postura.

    🔜 Interfaz gráfica amigable
    Visualización interactiva del desempeño durante la sesión.

    🔜 Exportación de reportes
    Generación de reportes PDF con gráficos y logs detallados.

8. 💡 Objetivo
   
    Mejorar la salud postural y productividad de personas que trabajan largas horas frente al computador, combinando inteligencia artificial, visión por computadora y principios de ergonomía.

9. 👨‍💻 Autor

    Desarrollado por: Juan David Rivaldo Diaz Sierra
   
    linkedin: https://www.linkedin.com/in/juan-david-rivaldo-diaz-sierra-72aa99222/
   
    Licencia: MIT
