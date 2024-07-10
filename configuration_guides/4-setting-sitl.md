# Instalación de la simuladora SITL de ArduPilot

1. Instalar las librerías necesarias en el sistema.
```
pip install -r requirements-simulator.txt
```
Si Cython, matplotlib o wxPython ya están instaladas, desinstálalas antes de ejecutar el comando.

2. Construir la simuladora siguiendo los pasos en la documentación de ArduPilot ([link](https://ardupilot.org/dev/docs/building-setup-linux.html)).

3. Ir al directorio del repositorio clonado y ejecutar `./waf configure --build sitl`.

4. Si el directorio `.tilecache` es propiedad de root, cambiar por el usuario.
