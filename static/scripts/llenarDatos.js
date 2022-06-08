function llenarDatos(empleado) {
  axios.get("http://127.0.0.1:5000/getEmpleado/" + empleado.id).then((res) => {
    document.querySelector("#idEmpleado").value = empleado.id;
    document.querySelector("#inputName-edit").value = res.data.nombre;
    document.querySelector("#inputApellido1-edit").value = res.data.apaterno;
    document.querySelector("#inputApellido2-edit").value = res.data.amaterno;
    document.querySelector("#inputMatricula-edit").value = res.data.matricula;
    document.querySelector("#selectPuesto-edit").value = res.data.puesto;
  });
}

function borrarDatos(event) {
  axios.post("/deleteempleado", {
    //id: event.previousElementSibling.id,
    id: event.value,
  });
}

// document
//   .getElementById("enviar-edit")
//   .addEventListener("click", function (event) {
//     event.preventDefault();
//   });
