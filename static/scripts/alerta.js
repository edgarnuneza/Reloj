if (localStorage.getItem("capturaOk") === "true") {
  console.log("ok");

  document.querySelector("#captura").innerHTML =
    '<div class="alert alert-success alert-dismissible fade show" role="alert">Fotografías registradas de forma correcta<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>';

  localStorage.removeItem("capturaOk");
}
