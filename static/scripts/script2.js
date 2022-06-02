let rostroPersona;

comprobacion = setInterval(comprobarCaptura, 500);

function comprobarCaptura() {
  axios.get("http://127.0.0.1:5000/rostroPersona").then((res) => {
    rostroPersona = res.data.rostro;
  });

  if (rostroPersona) {
    clearInterval(comprobacion);
    document.querySelector("#nombre").innerHTML = rostroPersona;
  }
}

let today = new Date();
let dd = String(today.getDate()).padStart(2, "0");
let mm = String(today.getMonth() + 1).padStart(2, "0");
let yyyy = today.getFullYear();
let hour = today.getHours();
let min = today.getMinutes();

min = min < 10 ? "0" + min : min;

today = `${dd}/${mm}/${yyyy} ${hour}:${min}`;

document.querySelector("#tiempo").innerHTML = today;
