OnRoad

¡Bienvenido a OnRoad Un emocionante juego de motocicletas en 2D que combina la tensión de la supervivencia en carretera con la adrenalina de las carreras de acrobacias con físicas realistas.

Este proyecto fue desarrollado utilizando Python y el framework Gale (Game Architecture & Logic Engine), basado en Pygame.

🎮 Modos de Juego y Jugabilidad

El juego cuenta con dos modos principales, accesibles desde la pantalla de título:

1. Modo Esquivar (1 Jugador)

Un modo de estilo endless runner donde el objetivo es llegar lo más lejos posible.

Jugabilidad: Conduces tu motocicleta por una carretera infinita. Debes esquivar obstáculos (piedras/charcos) que aparecen aleatoriamente y recolectar bidones de gasolina para mantener el tanque lleno.

Condición de Derrota: El juego termina si tu tanque de gasolina se vacía por completo (fuel <= 0) o si colisionas frontalmente contra un obstáculo.

Condición de Victoria / Progresión: No hay un "final", pero la distancia recorrida se traduce en puntos. Al alcanzar ciertos umbrales de puntos máximos en los High Scores (250, 500, 800), desbloquearás nuevas motocicletas en el garaje con mejores estadísticas (SBR, Enduro, Hyper Beast).

2. Modo Piruetas (2 Jugadores - Pantalla Dividida)

Una carrera competitiva cabeza a cabeza con físicas complejas utilizando gale.physics (basado en Pymunk).

Jugabilidad: Ambos jugadores compiten en un terreno generado proceduralmente (basado en curvas senoidales). Debes acelerar, frenar e inclinar tu moto en el aire para realizar flips (360°, 720°, etc.) que otorgan puntos extra. ¡Cuidado con hacer un caballito (wheelie) demasiado brusco o te caerás!

Condiciones de Derrota: Si un jugador cae de cabeza (colisión del chasis/piloto con el terreno) o cae al vacío, pierde la carrera inmediatamente. También puedes perder si se agota el tiempo límite una vez que el primer jugador cruza la meta.

Condición de Victoria: El primero en cruzar la meta (settings.GOAL_X) gana un bono de puntos enorme. Sin embargo, si el segundo jugador también cruza a tiempo, ¡el ganador se decide por el puntaje total (quien haya hecho mejores piruetas)!

⚙️ Controles

Modo 1 (Esquivar):

W / Flecha Arriba: Moverse hacia arriba (cambiar carril)

S / Flecha Abajo: Moverse hacia abajo

D / Flecha Derecha: Acelerar (consume más gasolina)

A / Flecha Izquierda: Frenar

P: Pausar el juego

Modo 2 (Piruetas - 2 Jugadores):

Jugador 1:

W / S: Acelerar / Frenar

A / D: Inclinar moto hacia atrás / adelante (en el aire)

Jugador 2:

Flecha Arriba / Abajo: Acelerar / Frenar

Flecha Izquierda / Derecha: Inclinar moto hacia atrás / adelante

Teclas Generales: Enter para confirmar selecciones en menús. Escape para salir.

🏗️ Arquitectura del Proyecto

El juego está construido bajo el patrón de diseño State Machine (Máquina de Estados) proporcionado por Gale. Esto permite aislar la lógica de cada pantalla (TitleState, BikeSelectState, OnRoadPlayState, RacingPlayState, etc.).

Físicas: El Modo 2 utiliza gale.physics.World y Joints (como WheelJoint con suspensión) para simular el comportamiento realista de las motos.

Gestión de Datos: Los puntajes altos se guardan localmente en el sistema del usuario (~/.onroad/highscores.dat).

Entrada (Input): Centralizado a través de gale.input_handler, mapeando teclas físicas a acciones lógicas (ej. KEY_w -> p1_accel).

🚀 Instalación y Ejecución

Para jugar, necesitas tener Python 3.9 o superior instalado en tu sistema. Se recomienda encarecidamente utilizar un entorno virtual.

1. Clonar el repositorio
```bash
git clone <https://github.com/frankz19/OnRoad>
cd OnRoad
```

2. Crear y activar el entorno virtual (Virtual Environment)

En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

En Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar las dependencias

Una vez activado el entorno virtual, instala Pygame y el motor Gale directamente desde su repositorio de GitHub:
```bash
pip install pygame
pip install git+https://github.com/R3mmurd/Gale
```


4. Ejecutar el juego
```bash
python main.py
```


📁 Distribución de Carpetas
```
OnRoad/
│
├── assets/                 # Recursos multimedia del juego
│   ├── fonts/              # Fuentes tipográficas (.ttf)
│   ├── graphics/           # Sprites, texturas y fondos (.png, .jpg)
│   ├── maps/               # Archivos de Tilemaps y configuraciones (.json, .tsx)
│   └── sounds/             # Música de fondo y efectos de sonido (.mp3, .wav, .ogg)
│
├── src/                    # Código fuente del juego
│   ├── states/             # Estados de la máquina de estados (Pantallas, Menús, Gameplay)
│   ├── utilities/          # Scripts de utilidad (Gestión de guardado de puntajes)
│   ├── Bike.py             # Clase de moto con físicas (Pymunk) para Modo 2
│   ├── GameObjects.py      # Objetos simples (obstáculos, gasolina) para Modo 1
│   ├── HighScoreManager.py # Lógica de desbloqueo de vehículos según puntaje
│   ├── Motorcycle.py       # Clase de moto arcade (sin físicas complejas) para Modo 1
│   ├── OnRoad.py           # Clase principal que hereda de gale.Game
│   ├── Terrain.py          # Generador de terreno procedural para Modo 2
│   └── World.py            # Gestor de colisiones, paralaje y spawn de objetos para Modo 1
│
├── .gitignore              # Archivos ignorados por Git
├── CHANGELOG.md            # Registro cronológico del desarrollo
├── main.py                 # Punto de entrada de la aplicación
├── save_data.json          # Datos persistentes adicionales
└── settings.py             # Configuraciones globales, inputs, colores y constantes
```