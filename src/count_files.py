import os
import json 

def count_found_people_pictures():
   """Counts how many pictures are currently saved
   in "found_people_captures".
   
   Returns:
      response_json: A string encoded in UTF-8 with
         the number of files found in the folder."""

   # Full route to the folder where the pictures featuring the found people are stored
   PICTURE_FOLDER_PATH = '/opt/flask-app/found_people_captures'

   program = f'ls {PICTURE_FOLDER_PATH} | wc -l'
   archivos = os.popen(program).read()

   # Getting the number of pictures in the folder
   response_data = {
      'numero_archivos': int(archivos)
   }
   response_json = json.dumps(response_data)
   return [response_json.encode('utf-8')]
