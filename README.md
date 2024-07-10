# TFG-reconocimiento-personas-dron

Eva Peso Adán (alu0101398037)

Desarrollado como TFG en la Universidad de La Laguna, curso 2023-2024.

Continuación del TFG "[Reconocimiento de imágenes por dron](https://github.com/Daniel-Arbelo/web-tfg-mod_wsgi/tree/main)" de Daniel Arbelo Hernández.

## Inicio

Este proyecto está hecho para ser desplegado en una Jetson Nano. El modelo usado fue la Jetson Nano Developer Kit 2GB.

### Configuración de la Jetson Nano

Los pasos pueden encontrarse [aquí](configuration_guides/1-setting-the-jetson.md).

### Configuración del servidor de apache

Los pasos para configurar el entorno virtual del servidor se encuentran [aquí](configuration_guides/2-setting-venv.md). Los pasos para configurar el servidor en sí se encuentran [aquí](configuration_guides/3-setting-apache.md).

## Simulando

La simuladora utilizada es la [SITL de ArduPilot](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html).

Cómo instalar la simuladora puede verse [aquí](configuration_guides/4-setting-sitl.md). Cómo usar la simuladora puede verse [aquí](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html).

## Clonar el repositorio

Para clonar el repositorio, simplemente es necesario hacer:

```
git clone https://github.com/epesoadan/TFG-reconocimiento-personas-dron.git
```

El proyecto está configurado para funcionar cuando el repositorio se encuentra dentro del directorio `/opt`.
