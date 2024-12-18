import { login, getProducts } from "./api.js";

// Evento para manejar el formulario de inicio de sesión
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorMessage = document.getElementById("error-message");

  // Reinicia el mensaje de error
  errorMessage.textContent = "";
  errorMessage.classList.add("hidden");

  try {
    const data = await login(username, password);
    alert(data.message || "Inicio de sesión exitoso.");
    window.location.href = "dashboard.html"; // Redirige al dashboard
  } catch (error) {
    console.error("Error en el login:", error.message);
    errorMessage.textContent = error.message;
    errorMessage.classList.remove("hidden");
  }
});


// Función para manejar el logout
async function logout() {
  try {
    localStorage.removeItem("token"); // Elimina el token del almacenamiento local
    alert("Sesión cerrada exitosamente.");
    window.location.href = "index.html"; // Redirige al inicio de sesión
  } catch (error) {
    alert("Ocurrió un problema al cerrar sesión.");
    console.error("Error durante el logout:", error);
  }
}

// Añade el evento al botón de logout
document.getElementById("logout-button").addEventListener("click", logout);

// Verifica si el usuario está autenticado al cargar productos
document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  if (!token) {
    alert("No estás autenticado. Inicia sesión.");
    window.location.href = "index.html";
  } else {
    loadProducts(); // Cargar los productos
  }
});

