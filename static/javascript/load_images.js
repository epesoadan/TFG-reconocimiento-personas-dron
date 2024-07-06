/** 
 * Generates a link to Google Maps.
 * @param {string} latitud The latitude of the coordinates
 * @param {string} longitud The longitude of the coordinates
 * @return {string} The link to Google Maps for that latitude and longitude.
 * 
 */
function generateMapLink(latitud, longitud) {
    return "https://www.google.com/maps/search/?api=1&query=" + latitud + "," + longitud;
}

/** 
 * Loads the images in the folder "found_people_captures" and its coordinates.
 * 
 */
function loadImages() {
    var imageContainer = document.getElementById("image-container");
    imageContainer.innerHTML = ""; // Cleans the image container

    // Path to the folder storing the files
    var folderPath = "found_people_captures/";

    // Calls "count_files.py"
    fetch('/countPictures', {
      method: 'POST'
    })
    .then(response => response.text())
    .then(data => {

      // Loads the coordinates info inside the coordinates file
      fetch('/coordenadas.txt')
      .then(response => response.text())
      .then(coordenadasData => {

        var coordenadas = coordenadasData.split('\n'); // Separates the lines in the file's text

        for (var i = 0; i < JSON.parse(data).numero_archivos; i++) {
          // Creates a container for the picture and its coordinates
          var imagenCoordenadasContainer = document.createElement("div");
          imagenCoordenadasContainer.className = "imagen-coordenadas-container";
          
          // Creates the image
          var imageSrc = folderPath + i + ".jpg";
          var imageElement = document.createElement("img");
          imageElement.className = "img-fluid"; //  Bootstrap class for columns
          imageElement.src = imageSrc;

          // Creates the link to Google Maps
          var [latitud, longitud] = coordenadas[i].split(","); // Separar latitud y longitud
          var mapLink = generateMapLink(latitud, longitud);

          var mapLinkElement = document.createElement("a");
          mapLinkElement.href = mapLink;
          mapLinkElement.target = "_blank"; // Opens the link in a new tab
          mapLinkElement.appendChild(imageElement);

          // Creates the coordinates
          var coordenadasElement = document.createElement("div");
          coordenadasElement.innerText = "Coordenadas: " + coordenadas[i]; // Gets the corresponding coords

          // Adds the image and its coordinates to the container
          imagenCoordenadasContainer.appendChild(mapLinkElement);
          imagenCoordenadasContainer.appendChild(coordenadasElement);
          imagenCoordenadasContainer.className = "col-12 col-md-4 mt-4"; // Bootstrap for responsive columns

          imageContainer.appendChild(imagenCoordenadasContainer);
        }
      })
    })
    .catch(error => {
      console.error('Error:', error);
    });
}