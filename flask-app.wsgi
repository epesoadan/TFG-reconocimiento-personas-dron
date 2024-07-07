import sys
import os
import site

site.addsitedir('/opt/flask-app/flask-venv/lib/python3.7/site-packages')
sys.path.insert(0,'/opt/flask-app')

# Fija la variable de entorno para el entorno virtual
os.environ['VIRTUAL_ENV'] = '/opt/flask-app/flask-venv'
os.environ['PATH'] = f"/opt/flask-app/flask-venv/bin:{os.environ['PATH']}"

# Redefine sys.executable para asegurar que los scripts se ejecuten en el entorno virtual
sys.executable = '/opt/flask-app/flask-venv/bin/python3.7'

# Crea un log que muestra el contenido de las variables
# para asegurar que tengan el valor correcto
with open('/tmp/wsgi_debug.log', 'w') as f:
    f.write(f"sys.path: {sys.path}\n")
    f.write(f"VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV')}\n")
    f.write(f"PATH: {os.environ.get('PATH')}\n")

from app import app as application
