let empleado;
let today = new Date();
let dd = String(today.getDate()).padStart(2, "0");
let mm = String(today.getMonth() + 1).padStart(2, "0");
let yyyy = today.getFullYear();
let hour = today.getHours();
let min = today.getMinutes();

min = min < 10 ? "0" + min : min;

today = `${dd}/${mm}/${yyyy} ${hour}:${min}`;

//document.querySelector("#tiempo").innerHTML = today;


// document.querySelector("#nombre").innerHTML = "Chris Evans";

axios.get("/api/empleadoactual").then((res) => {
    empleado = res.data;
    document.querySelector("#nombre").innerHTML = empleado.nombre;
    document.querySelector("#tiempo").innerHTML = today;
});

const btnEntrada = document.querySelector("#entrada");
const btnSalida = document.querySelector("#salida");

btnEntrada.addEventListener('click', () => {
    if(empleado.id !== null)
    {
        axios.post("/registrarmovimiento", {
            id_empleado:  empleado.id, 
            tipo: 'Entrada'
        }).then(() => {
            window.location.href = "/verMovimientos/" + empleado.id;
        });
    }
});

btnSalida.addEventListener('click', () => {
    if(empleado.id !== null)
    {
        axios.post("/registrarmovimiento", {
            id_empleado:  empleado.id, 
            tipo: 'Salida'
        }).then(() => {
            window.location.href = "/verMovimientos/" + empleado.id;
        });
    }
});