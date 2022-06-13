let isCaptured;

comprobacion = setInterval(comprobarCaptura, 500);

function comprobarCaptura() {
  axios.get("/api/count").then((res) => {
    rostroPersona = res.data.isCaptured;
  });

  if (rostroPersona) {
    clearInterval(comprobacion);
    window.location.href = "registro";
  }
}
