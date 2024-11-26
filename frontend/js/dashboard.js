//carga los productos al cargar la pagina
document.addEventListener("DOMContentLoaded", loadProducts);

//boton de cerrar sesion
document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("token"); //elimina el token
  window.location.href = "index.html"; //redirige al login
});

//mostrar y ocultar el modal
const modal = document.getElementById("product-modal");
const addProductBtn = document.getElementById("add-product-btn");
const cancelBtn = document.getElementById("cancel-btn");

addProductBtn.addEventListener("click", () => {
  modal.classList.remove("hidden"); //muestra el modal
});

cancelBtn.addEventListener("click", () => {
  modal.classList.add("hidden"); //oculta el modal
});

//enviar el formulario para agregar un producto
document.getElementById("add-product-form").addEventListener("submit", async (e) => {
  e.preventDefault(); //evita la recarga de la página

  //captura los datos del formulario
  const name = document.getElementById("product-name").value;
  const description = document.getElementById("product-description").value;
  const price = parseFloat(document.getElementById("product-price").value);
  const stock = parseInt(document.getElementById("product-stock").value);

  try {
    await addProduct({ name, description, price, stock }); //llama a la funcion en api.js
    alert("Producto agregado exitosamente");
    modal.classList.add("hidden"); //cierra el modal
    loadProducts(); //recarga la tabla de productos
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
});

//carga productos desde la API y mostrarlos en la tabla
async function loadProducts() {
  try {
    const products = await getProducts(); //funcion en api.js
    const table = document.getElementById("product-table");

    //limpia la tabla antes de llenarla
    table.innerHTML = "";

    //agrega cada producto como fila
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
