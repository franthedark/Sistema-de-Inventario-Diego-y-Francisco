// Carga los productos al cargar la página
document.addEventListener("DOMContentLoaded", async () => {
  try {
    await loadProducts();
  } catch (error) {
    console.error("Error al cargar los productos:", error);
    alert("No se pudieron cargar los productos. Verifica la conexión con el servidor.");
  }
});

async function loadProducts() {
  try {
    const response = await fetch("/productos");

    if (!response.ok) {
      throw new Error("Error al obtener los productos del servidor.");
    }

    const products = await response.json();
    const table = document.getElementById("product-table");

    // Limpiar la tabla antes de llenarla
    table.innerHTML = "";

    // Agregar filas dinámicamente
    products.forEach((product) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td class="py-2 px-4 border">${product.nombre}</td>
        <td class="py-2 px-4 border">${product.descripcion}</td>
        <td class="py-2 px-4 border">$${parseFloat(product.precio).toFixed(0)}</td>
        <td class="py-2 px-4 border">${product.stock}</td>
        <td class="py-2 px-4 border">
          <button class="deactivate-btn bg-red-500 text-white py-1 px-3 rounded" data-id="${product.id}">
            Desactivar
          </button>
        </td>
      `;
      table.appendChild(row);
    });

    // Asignar eventos a los botones de Desactivar
    document.querySelectorAll(".deactivate-btn").forEach((button) => {
      button.addEventListener("click", () => deactivateProduct(button.dataset.id));
    });
  } catch (error) {
    console.error("Error al cargar los productos:", error);
    alert("No se pudieron cargar los productos. Verifica la conexión con el servidor.");
  }
}


// Función para desactivar un producto
async function deactivateProduct(id) {
  if (!confirm("¿Estás seguro de que deseas desactivar este producto?")) return;

  try {
    const response = await fetch(`/productos/${id}/desactivar`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error("Error al desactivar el producto.");
    }

    alert("Producto desactivado exitosamente.");
    loadProducts(); // Recargar la lista de productos
  } catch (error) {
    console.error("Error al desactivar el producto:", error);
    alert("No se pudo desactivar el producto. Inténtalo de nuevo.");
  }
}

// Botón de cerrar sesión
document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("token"); // Elimina el token
  window.location.href = "index.html"; // Redirige al login
});

// Mostrar y ocultar el modal para agregar productos
const productModal = document.getElementById("product-modal");
const addProductBtn = document.getElementById("add-product-btn");
const cancelProductBtn = document.getElementById("cancel-btn");

addProductBtn.addEventListener("click", () => {
  productModal.classList.remove("hidden"); // Muestra el modal
});

cancelProductBtn?.addEventListener("click", () => {
  productModal.classList.add("hidden"); // Oculta el modal
});

// Modal para registrar compras/ventas
const transactionModal = document.getElementById("transaction-modal");
const addTransactionBtn = document.getElementById("add-transaction-btn");
const cancelTransactionBtn = document.getElementById("cancel-transaction");

addTransactionBtn.addEventListener("click", () => {
  loadProductOptions(); // Carga las opciones de productos
  transactionModal.classList.remove("hidden");
});

cancelTransactionBtn.addEventListener("click", () => {
  transactionModal.classList.add("hidden");
});

// Botón para generar el reporte de ventas
document.getElementById("generate-report-btn").addEventListener("click", async () => {
  try {
    const response = await fetch("/api/sales-report");
    if (!response.ok) {
      throw new Error("Error al generar el reporte");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "reporte_ventas.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    alert("Reporte generado exitosamente");
  } catch (error) {
    console.error("Error al generar el reporte:", error);
    alert("Hubo un problema al generar el reporte. Por favor, inténtalo de nuevo.");
  }
});

// Función para cargar opciones de productos
async function loadProductOptions() {
  try {
    const response = await fetch("/productos");
    if (!response.ok) {
      throw new Error("Error al obtener las opciones de productos");
    }

    const products = await response.json();
    const productSelect = document.getElementById("product");

    productSelect.innerHTML = "";

    products.forEach((product) => {
      const option = document.createElement("option");
      option.value = product.id;
      option.textContent = product.nombre;
      productSelect.appendChild(option);
    });
  } catch (error) {
    console.error("Error al cargar las opciones de productos:", error);
    alert("No se pudieron cargar las opciones de productos.");
  }
}

// Nueva función para manejar las transacciones (compra/venta)
async function handleTransaction(transactionData) {
  const token = localStorage.getItem("token");

  try {
    const response = await fetch(`${API_URL}/${transactionData.type === "venta" ? "ventas" : "compras"}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(transactionData),
    });

    // Validar el estado de la respuesta
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error en la respuesta del servidor:", errorData);
      throw new Error(errorData.message || "Error al procesar la transacción");
    }

    const result = await response.json();
    console.log("Respuesta del servidor:", result);

    alert(`${transactionData.type === "venta" ? "Venta" : "Compra"} registrada exitosamente`);
    
    // Recargar los productos para reflejar el stock actualizado
    await loadProducts();
  } catch (error) {
    console.error("Error en la transacción:", error.message);
    alert("Hubo un problema al registrar la transacción. Inténtalo de nuevo.");
  }
}


// Modificar el evento del formulario de transacciones
document.getElementById("transaction-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const productId = document.getElementById("product").value;
  const quantity = parseInt(document.getElementById("quantity").value, 10);
  const transactionType = document.querySelector('input[name="transaction-type"]:checked').value;

  if (!productId || !quantity || !transactionType) {
    alert("Por favor, completa todos los campos.");
    return;
  }

  const transactionData = {
    type: transactionType,
    detalles: [{ producto_id: productId, cantidad: quantity }],
  };

  await handleTransaction(transactionData);
});
