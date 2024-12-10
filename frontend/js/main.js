//selecciona el formulario y añade un manejador de eventos
document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault(); //evita el envio del formulario por defecto
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
//funcion para manejar el logout
async function logout() {
  try {
    const result = await login(username, password); //llama a la funcion de login desde api.js
    alert("Inicio de sesión exitoso"); //muestra un mensaje de exito
    window.location.href = "dashboard.html"; //redirige al panel principal
    //envia solicitud al endpoint de logout del backend
    const response = await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include' //incluye cookies en la solicitud
    });
    if (response.ok) {
      alert("Sesión cerrada exitosamente.");
      window.location.href = "index.html"; //redirige al inicio de sesión
    } else {
      alert("Error al cerrar sesión.");
    }
  } catch (error) {
    alert(`Error: ${error.message}`); //muestra un mensaje de error al usuario
    console.error("Error durante el logout:", error);
    alert("Ocurrió un problema al cerrar sesión.");
  }
//logout
document.getElementById("logout-button").addEventListener("click", logout);
