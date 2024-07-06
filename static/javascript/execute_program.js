let updateInterval

/** 
 * Function that starts the camera detection program
 * through the graphical interface, and also shows
 * the current content of the program's log file.
 * 
 */
function executeProgram() {
    // Hides button
    document.getElementById("myButton").classList.add("d-none");
    document.getElementById("loadingCircle").classList.remove("d-none");
    document.getElementById('log-console').classList.remove("d-none");
    document.getElementById('resultado').innerText = "Ejecutando programa de detección de personas, esto puede tardar unos minutos hasta que comience a funcionar";
    
    // Calls "execute_program.py"
    fetch('/executeProgram')
    .then(response => response.text())
    .then(data => {
        // Shows the result of the program
        document.getElementById("myButton").classList.remove("d-none");
        document.getElementById("loadingCircle").classList.add("d-none");
        document.getElementById("resultado").innerText = data;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("myButton").classList.remove("d-none");
        document.getElementById("loadingCircle").classList.add("d-none");
        document.getElementById("resultado").innerText = 'Error al ejecutar el programa.';
    });

    // Starts the log console
    updateInterval = setInterval(() => {
        fetch('/logs')
        .then(response => response.text())
        .then(logData => {
            document.getElementById('log-console').innerText = logData;
        })
        .catch(error => {
            console.error('Error al leer el archivo de log:', error);
        });
    }, 1000); // Reads the file every second
  }