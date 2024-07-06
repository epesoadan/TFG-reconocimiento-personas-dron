/** 
 * Function that checks the drone connectivity
 * through the graphical interface.
 * 
 */
function checkDroneConnection() {
    // Hides button
    document.getElementById("myButton3").classList.add("d-none");
    document.getElementById("loadingCircle3").classList.remove("d-none");
    document.getElementById('resultado3').innerText = "Comprobando conectividad";
    // Calls "controller_info.py"
    fetch('/checkController')
    .then(response => response.text())
    .then(data => {
      // Shows the result of the program
      document.getElementById("myButton3").classList.remove("d-none");
      document.getElementById("loadingCircle3").classList.add("d-none");
      document.getElementById('resultado3').innerText = data;
    })
    .catch(error => {
      console.error('Error:', error);
    });

}