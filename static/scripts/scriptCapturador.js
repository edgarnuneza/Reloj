let isCaptured;
let rostroPersona;

comprobacion = setInterval(comprobarCaptura, 500);

function comprobarCaptura() {
  axios.get("/api/countcaptura").then((res) => {
    console.log(res);
    rostroPersona = res.data.detener;
  });

  if (rostroPersona) {
    clearInterval(comprobacion);
    localStorage.setItem('capturaOk', 'true');
    window.location.href = "/empleados";
  }
}