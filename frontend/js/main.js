//selecciona el formulario y anade un manejador de eventos
document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault(); //evita el envío del formulario por defecto

  //captura los valores del formulario
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const result = await login(username, password); //llama a la funcion de login desde api.js
    alert("Inicio de sesión exitoso"); //muestra un mensaje de exito
    window.location.href = "dashboard.html"; //redirige al panel principal
  } catch (error) {
    alert(`Error: ${error.message}`); //muestra un mensaje de error al usuario
    console.error("Error durante el inicio de sesión:", error);
  }
});

// Función para manejar el logout
async function logout() {
  try {
    // envia solicitud al endpoint de logout del backend
    const response = await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include', //incluye cookies en la solicitud
    });

    if (response.ok) {
      alert("Sesión cerrada exitosamente.");
      window.location.href = "index.html"; //redirige al inicio de sesion
    } else {
      alert("Error al cerrar sesión.");
    }
  } catch (error) {
    alert("Ocurrió un problema al cerrar sesión.");
    console.error("Error durante el logout:", error);
  }
}

//anade el evento al boton de logout
document.getElementById("logout-button").addEventListener("click", logout);
