const API_URL = "http://127.0.0.1:8000"; //URL del backend

// Función iniciar sesión
export async function login(username, password) {
  try {
    const response = await fetch(`${API_URL}/users/login`, {
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

    // Almacenar el token si es necesario
    if (data.token) {
      localStorage.setItem("token", data.token);
    }

    return data; // Devuelve los datos para manejarlos en el frontend
  } catch (error) {
    console.error("Error en login:", error.message);
    throw new Error("No se pudo conectar al servidor. Inténtalo de nuevo más tarde.");
  }
}


// Función obtener productos
async function getProducts() {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("No se encontró el token de autenticación.");
  }

  const response = await fetch(`${API_URL}/productos`, {
    headers: {
      Authorization: `Bearer ${token}`, // Incluye el token para la autenticación
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "Error al obtener productos");
  }

  return await response.json();
}

// Exportar las funciones
export { login, getProducts };


//funcion agregar un producto
async function addProduct(product) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${API_URL}/productos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`, //incluye el token
    },
    body: JSON.stringify(product),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "Error al agregar el producto");
  }

  return response.json();
}

//funcion registrar una transaccion (compra o venta)
async function addTransaction(transaction) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${API_URL}/ventas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`, //incluye el token
    },
    body: JSON.stringify(transaction),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "Error al registrar la transacción");
  }

  return response.json();
}

//funcion generar reporte de ventas
async function generateSalesReport() {
  const token = localStorage.getItem("token");
  const response = await fetch(`${API_URL}/reportes/reporte-ventas`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`, //incluye el token
    },
  });

  if (!response.ok) {
    throw new Error("Error al generar el reporte de ventas.");
  }

  return response.blob(); //retorna el archivo como blob
}

//funcion registrar una compra
async function addPurchase(purchase) {
  const token = localStorage.getItem("token");
  const response = await fetch(`${API_URL}/compras`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`, //incluye el token
    },
    body: JSON.stringify(purchase),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "Error al registrar la compra");
  }

  return response.json();
}