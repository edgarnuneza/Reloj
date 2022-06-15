function llenarDatos(empleado) {
  axios.get("/getEmpleado/" + empleado.id).then((res) => {
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
    id: event.value,
  });
}

