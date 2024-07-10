# Configurando el entorno virtual
1. Instala Jetson-Inference siguiendo los pasos dados en el repositorio ([link](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md)).

2. Crear el entorno virtual usando Python 3.7.
```
python3.7 -m venv flask-venv
```

3. Instala las librerías requeridas dentro del entorno.
```
pip install -r requirements-venv.txt
```

4. Transferir los archivos de Jetson-inference al entorno virtual.
```
cp /usr/lib/python3.7/dist-packages/jetson_utils_python.so /opt/flask-app/flask-venv/lib/python3.7/site-packages
cp /usr/lib/python3.7/dist-packages/jetson_inference_python.so /opt/flask-app/flask-venv/lib/python3.7/site-packages
cp -r /usr/lib/python3.7/dist-packages/jetson /opt/flask-app/flask-venv/lib/python3.7/site-packages
cp -r /usr/lib/python3.7/dist-packages/Jetson /opt/flask-app/flask-venv/lib/python3.7/site-packages
cp -r /usr/lib/python3.7/dist-packages/jetson_utils /opt/flask-app/flask-venv/lib/python3.7/site-packages
cp -r /usr/lib/python3.7/dist-packages/jetson_inference /opt/flask-app/flask-venv/lib/python3.7/site-packages
```

Si el entorno virtual está en otra parte que no sea `/opt/flask-app`, o si no se llama `flask-venv`, hay que editar los archivos `flask.conf` y `flask-app.wsgi` para que tengan la ruta correcta.