const API_URL = "http://127.0.0.1:8000"; //URL del backend

//funcion iniciar sesion
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
      Authorization: `Bearer ${token}`, //incluye el token para la autenticacion
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
  const response = await fetch(`${API_URL}/reportes/ventas`, {
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