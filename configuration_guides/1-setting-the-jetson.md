# Configurando la Jetson Nano

1. Instalar Python 3.7. El proyecto está pensado para esta versión en particular.
```
sudo apt-get update
sudo apt-get install python3.7
sudo apt-get install python3.7-dev
```

2. Covertir Python 3.7 en la versión por defecto
```
sudo ln -sf /usr/bin/python3.7 /usr/bin/python
sudo ln -sf /usr/bin/python3.7 /usr/bin/python3
```

3. Instalar otros paquetes de Python necesarios
```
sudo apt-get install python3-pip
sudo apt-get install python3-venv
sudo apt-get install v4l-utils
```

4. Instalar librerías de Python necesarias
```
/usr/bin/python3.7 -m pip install --upgrade pip
pip install future
pip install pyserial
pip install pymavlink
pip install MAVProxy
```