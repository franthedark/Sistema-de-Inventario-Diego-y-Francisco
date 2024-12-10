//carga los productos al cargar la página
document.addEventListener("DOMContentLoaded", () => {
  loadProducts();
});

//boton de cerrar sesion
document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("token"); //elimina el token
  window.location.href = "index.html"; //redirige al login
});

//mostrar y ocultar el modal para agregar productos
const productModal = document.getElementById("product-modal");
const addProductBtn = document.getElementById("add-product-btn");
const cancelProductBtn = document.getElementById("cancel-btn");

addProductBtn.addEventListener("click", () => {
  productModal.classList.remove("hidden"); //muestra el modal
});

cancelProductBtn.addEventListener("click", () => {
  productModal.classList.add("hidden"); //oculta el modal
});

//modal para registrar compras/ventas
const transactionModal = document.getElementById("transaction-modal");
const addTransactionBtn = document.getElementById("add-transaction-btn");
const cancelTransactionBtn = document.getElementById("cancel-transaction");

//boton para generar el reporte de ventas
document.getElementById("generate-report-btn").addEventListener("click", async () => {
  try {
    const response = await fetch("/api/sales-report"); //llama al endpoint del reporte
    if (!response.ok) {
      throw new Error("Error al generar el reporte");
    }

    const blob = await response.blob(); //obtiene el archivo como blob
    const url = window.URL.createObjectURL(blob); //crea una URL para descargarlo
    const a = document.createElement("a");
    a.href = url;
    a.download = "reporte_ventas.pdf"; //nombre del archivo
    document.body.appendChild(a);
    a.click();
    a.remove();
    alert("Reporte generado exitosamente");
  } catch (error) {
    console.error("Error al generar el reporte:", error);
    alert("Hubo un problema al generar el reporte. Por favor, inténtalo de nuevo.");
  }
});

//mostrar y ocultar el modal de transacciones
addTransactionBtn.addEventListener("click", () => {
  loadProductOptions(); //carga las opciones de productos
  transactionModal.classList.remove("hidden");
});

cancelTransactionBtn.addEventListener("click", () => {
  transactionModal.classList.add("hidden");
});

//enviar el formulario para registrar una transacción
document.getElementById("transaction-form").addEventListener("submit", async (e) => {
  e.preventDefault(); // Evita la recarga de la página

  //captura los datos del formulario
  const product = document.getElementById("product").value;
  const quantity = parseInt(document.getElementById("quantity").value);
  const type = document.querySelector("input[name='transaction-type']:checked").value;

  try {
    await addTransaction({ product, quantity, type }); //llama a la función en api.js
    alert("Transacción registrada exitosamente");
    transactionModal.classList.add("hidden"); //cierra el modal
    loadProducts(); //recarga la tabla de productos
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
});

//enviar el formulario para agregar un producto
document.getElementById("add-product-form").addEventListener("submit", async (e) => {
  e.preventDefault(); //evita la recarga de la pagina

  //captura los datos del formulario
  const name = document.getElementById("product-name").value;
  const description = document.getElementById("product-description").value;
  const price = parseFloat(document.getElementById("product-price").value);
  const stock = parseInt(document.getElementById("product-stock").value);

  try {
    await addProduct({ name, description, price, stock }); //llama a la funcion en api.js
    alert("Producto agregado exitosamente");
    productModal.classList.add("hidden"); //cierra el modal
    loadProducts(); //recarga la tabla de productos
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
});

//cargar opciones de productos para transacciones
async function loadProductOptions() {
  try {
    const products = await getProducts(); //funcion en api.js
    const productSelect = document.getElementById("product");

    //limpiar opciones existentes
    productSelect.innerHTML = "";

    //agregar opciones dinamicas
    products.forEach((product) => {
      const option = document.createElement("option");
      option.value = product.id;
      option.textContent = product.name;
      productSelect.appendChild(option);
    });
  } catch (error) {
    console.error("Error al cargar opciones de productos:", error);
    alert("Hubo un error al cargar los productos. Por favor, inténtalo de nuevo.");
  }
}

//cargar productos desde la API y mostrarlos en la tabla
async function loadProducts() {
  try {
    const products = await getProducts(); //funcion en api.js
    const table = document.getElementById("product-table");

    //limpiar la tabla antes de llenarla
    table.innerHTML = "";

    //agregar producto como fila
    products.forEach((product) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td class="py-2 px-4 border">${product.name}</td>
        <td class="py-2 px-4 border">${product.description}</td>
        <td class="py-2 px-4 border">$${product.price.toFixed(2)}</td>
        <td class="py-2 px-4 border">${product.stock}</td>
        <td class="py-2 px-4 border">
          <button class="bg-blue-500 text-white py-1 px-3 rounded mr-2">Editar</button>
          <button class="bg-red-500 text-white py-1 px-3 rounded">Eliminar</button>
        </td>
      `;
      table.appendChild(row);
    });
  } catch (error) {
    console.error("Error al cargar los productos:", error);
    alert("Hubo un error al cargar los productos. Por favor, inténtalo de nuevo.");
  }
}
