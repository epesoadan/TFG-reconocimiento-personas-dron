# Configurando el servidor apache2
1. Instalar los paquetes necesarios.
```
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
```

2. Mueve el archivo `flask.conf` de este directorio a `/etc/apache2/sites-available`.

3. Iniciar apache y mod-wsgi
```
sudo service apache2 start
sudo a2ensite flask
sudo a2enmod wsgi
```

4. Reiniciar el servidor (hay que hacer esto cada vez que se cambie un programa para que se reflejen los cambios).
```
sudo systemctl restart apache2
```

5. Dar permisos al usuario `www-data` para que este pueda acceder a los directorios del proyecto y ejecutar todos los programas que hay dentro.

6. Darle una contraseña a `www-data` con `sudo passwd www-data`.

Si el proyecto no está en `/opt/flask-app`, hay que editar los archivos `flask.conf` y `flask-app.wsgi` para que tengan las rutas adecuadas.