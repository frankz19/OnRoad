Changelog - OnRoad



[1.0.0] - Lanzamiento Final

Añadido

Modo Racing (2 Jugadores): Implementada la pantalla dividida dinámica.

Sistema de acrobacias (Stunts): Detección matemática de giros en el aire (360°, 720°, 1080°) que otorgan puntos extra y muestran popups coloridos de confirmación (FlipPopup).

Audio Dinámico de Motores: Creada la clase EngineSound que varía el volumen del motor en tiempo real dependiendo de si el jugador está acelerando o no.

Muerte Súbita (Timeout): Al cruzar el primer jugador la meta, se activa una cuenta regresiva estricta de 10 segundos para el segundo jugador.

Modificado

Refactorización de la gestión de audio en OnRoad.py y los diferentes States para asegurar que la música se detenga y cambie correctamente al entrar o salir de las partidas (evitando el solapamiento de pistas).

Balanceo de la velocidad de caída y fuerza de salto de las motos en el aire.

Arreglado

Corregido el bug donde los Popups de las piruetas se dibujaban fuera de los límites de las cámaras en la pantalla dividida.

Ajustes en Terrain.py para evitar que la generación procedural creara barrancos imposibles de subir justo en la línea de salida (FLAT_START).

[0.9.0] - Ajustes de Física y Pantalla Dividida

Añadido

Integración oficial del motor de físicas usando gale.physics.world.

Implementación de cámara con zoom-out (factor de 3x) utilizando pygame.Surface de alta resolución antes de escalar a la pantalla virtual, permitiendo ver mejor los saltos.

Control direccional en el aire (AIR_TILT_TORQUE) para permitir rotaciones.

Arreglado

Corregido el cálculo del centro de masa y la suspensión en Bike.py. Se ajustaron los parámetros de WheelJoint (SUSPENSION_FREQUENCY y SUSPENSION_DAMPING) para evitar que las motos "explotaran" o se hundieran en pendientes extremas.

Añadida lógica Anti-Wheelie para evitar que las motos se volteen solas al acelerar en terreno plano.

[0.8.0] - Modo Racing: Terreno Procedural y Vehículos

Añadido

Clase Terrain.py que genera polígonos estáticos (PolygonShape) para el suelo basados en la combinación de ondas senoidales matemáticas para simular colinas suaves y picos extremos.

Clase Bike.py construida con un chasis (BoxShape) y dos ruedas (CircleShape), unidos por articulaciones de rueda.

Lógica para detectar si las ruedas de la moto están tocando el suelo (_has_wheel_contact) para permitir o denegar los giros en el aire.

[0.7.0] - Progresión, Garaje y Guardado de Datos

Añadido

Sistema persistente de High Scores en utilities/highscores.py que guarda los récords de los jugadores en un archivo local (~/.onroad/highscores.dat).

Pantalla de Garaje (BikeSelectState.py) con visualización de motos.

Lógica de desbloqueo dinámico en HighScoreManager.py: Las motos SBR, Enduro y Hyper Beast ahora requieren 250, 500 y 800 puntos respectivamente.

Modificado

El estado GameOverState ahora alerta visualmente si el jugador alcanzó un nuevo umbral de puntos y desbloqueó un vehículo.

[0.6.0] - Sistema de Puntuaciones Arcade

Añadido

Creado el estado EnterHighScoreState.py que permite ingresar iniciales de 3 letras rotando el abecedario, al estilo de las máquinas arcade clásicas.

Creado el estado HighScoreState.py para visualizar el podio de los 10 mejores jugadores.

[0.5.0] - Modo Esquivar: Pulido y Colisiones

Añadido

Incorporados Sprites y Frames de la hoja de texturas de obstáculos usando los utilitarios de recortes.

Animación y efectos de sonido para la recolección de gasolina (bonus.wav) y explosiones por choques.

Implementada la lógica de Game Over directa si el jugador se queda sin combustible (motorcycle.fuel <= 0).

Arreglado

El movimiento de los objetos en World.py ahora se escala correctamente con el dt (delta time) para asegurar que la dificultad aumente suavemente y no dependa de los FPS del monitor.

[0.4.0] - Modo Esquivar: Obstáculos y Combustible

Añadido

Creado el gestor World.py para el Modo Esquivar.

Fondo infinito con efecto Parallax Scrolling simulando profundidad (cielo moviéndose más lento que la carretera).

Generador (Spawner) aleatorio de la clase GameObject.py (Obstáculos y Bidones de Gasolina) con tiempos de aparición (spawn_timer) que disminuyen a medida que el jugador sobrevive más tiempo.

[0.3.0] - Modo Esquivar: Controles Base

Añadido

Clase Motorcycle.py (Modelo Arcade, sin físicas de Pymunk).

Implementados movimientos en X (Acelerar/Frenar) e Y (Cambio de Carril) usando interpolación lineal matemática con inercia y fricción.

Sistema de drenaje de combustible que aumenta al mantener presionado el acelerador.

Limitadores de pantalla para evitar que el jugador salga de los bordes superior e inferior de la carretera.

[0.2.0] - Arquitectura Base y Máquina de Estados

Añadido

Configuración global del proyecto en settings.py (Resoluciones virtuales, fuentes, mapeo de controles).

Inicialización del entorno con el motor Gale (gale.game.Game).

Implementada la Arquitectura de Máquina de Estados (StateMachine) en la clase principal OnRoad.py.

Creados los estados base funcionales: TitleScreenState y la estructura inicial del bucle de juego.

Sistema centralizado de Inputs usando gale.input_handler para soportar configuraciones de teclado.

[0.1.0] - Inicio del Proyecto

Añadido

Repositorio inicializado.

Estructura de carpetas creada (assets/, src/, src/states/).

Cargados los primeros assets de prueba (imágenes de vehículos, texturas placeholder y música temporal).