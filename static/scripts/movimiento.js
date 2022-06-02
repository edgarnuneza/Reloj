let today = new Date();
let dd = String(today.getDate()).padStart(2, "0");
let mm = String(today.getMonth() + 1).padStart(2, "0");
let yyyy = today.getFullYear();
let hour = today.getHours();
let min = today.getMinutes();

min = min < 10 ? "0" + min : min;

today = `${dd}/${mm}/${yyyy} ${hour}:${min}`;
