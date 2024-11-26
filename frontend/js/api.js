const API_URL = "http://localhost:8000"; //hay que poner la url del back

//función iniciar sesion
async function login(username, password) {
  try {
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || "Error al iniciar sesión");
    }

    const data = await response.json();
    localStorage.setItem("token", data.token); //guarda el token
    return data;
  } catch (error) {
    console.error("Error en login:", error.message);
    throw error;
  }
}

//funcion obtener productos
async function getProducts() {
  const token = localStorage.getItem("token");
  const response = await fetch(`${API_URL}/products`, {
    headers: {
      Authorization: `Bearer ${token}`, //incluye el token para la autenticación
    },
  });

  if (!response.ok) {
    throw new Error("No se pudieron cargar los productos.");
  }

  return response.json();
}

//funcion agregar un producto
async function addProduct(product) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${API_URL}/products`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`, // Incluye el token
    },
    body: JSON.stringify(product),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "Error al agregar el producto");
  }

  return response.json();
}
