/** 
 * Function that stops the camera detection program
 * through the graphical interface.
 * 
 */
function closeProgram() {
    clearInterval(updateInterval);
    // Hide button
    document.getElementById("myButton2").classList.add("d-none");
    document.getElementById("loadingCircle2").classList.remove("d-none");
    // Calls "stop_program.py"
    fetch('/finishProgram', {
      method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
      // Shows the output in the interface
      document.getElementById('resultado2').innerText = data;
      document.getElementById("loadingCircle2").classList.add("d-none");
      document.getElementById("myButton2").classList.remove("d-none");
      document.getElementById('resultado').innerText = "";
      document.getElementById('log-console').classList.add('d-none');
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }