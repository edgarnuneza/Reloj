let isCaptured;

comprobacion = setInterval(comprobarCaptura, 500);

function comprobarCaptura() {
  axios.get("http://127.0.0.1:5000/api/count").then((res) => {
    rostroPersona = res.data.isCaptured;
  });

  if (rostroPersona) {
    clearInterval(comprobacion);
    window.location.href = "registro";
  }
}
