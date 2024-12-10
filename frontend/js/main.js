//funcion para manejar el logout
async function logout() {
  try {
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
    console.error("Error durante el logout:", error);
    alert("Ocurrió un problema al cerrar sesión.");
  }
}
//logout
document.getElementById("logout-button").addEventListener("click", logout);
