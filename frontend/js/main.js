//selecciona el formulario y añade un manejador de eventos
document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault(); //evita el envio del formulario por defecto

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const result = await login(username, password); //llama a la funcion de login desde api.js
    alert("Inicio de sesión exitoso"); //muestra un mensaje de exito
    window.location.href = "dashboard.html"; //redirige al panel principal
  } catch (error) {
    alert(`Error: ${error.message}`); //muestra un mensaje de error al usuario
  }
});
