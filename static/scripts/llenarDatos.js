function llenarDatos(empleado) {
  axios.get("/getEmpleado/" + empleado.id).then((res) => {
    document.querySelector("#idEmpleado").value = empleado.id;
    document.querySelector("#inputName-edit").value = res.data.nombre;
    document.querySelector("#inputApellido1-edit").value = res.data.apaterno;
    document.querySelector("#inputApellido2-edit").value = res.data.amaterno;
    document.querySelector("#inputMatricula-edit").value = res.data.matricula;
    //document.querySelector("#selectPuesto-edit").value = res.data.puesto;
    document.getElementById('editPuestos').selectedIndex=indicePuesto(res.data.puesto)
  });
}
function indicePuesto(puesto){
  for(x=0;x<document.getElementById('editPuestos').children.length;x++){
    if(document.getElementById('editPuestos').children[x].text==puesto){
     break
     
    }
  }
  return x
}
function pedirPuesto(puesto){
  axios.get("/getPuesto/"+puesto)((res) => {
    document.querySelector("#idEmpleado").value = empleado.id;
    document.getElementById('editPuestos').selectedIndex=2 
  });
}

function borrarDatos(event) {
  axios.post("/deleteempleado", {
    id: event.value,
  });
}
/*Aqui estara la funcion de puestos */
function llenarPuestos(){
  console.log("Mensaje de llenarPuestos")
}
