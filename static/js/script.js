document.getElementById('servicio-form').addEventListener('submit', function (e) {
    e.preventDefault();
    
    // Obtener los valores del formulario
    const nombre = document.getElementById('nombre').value;
    const categoria = document.getElementById('categoria').value;
    const descripcion = document.getElementById('descripcion').value;
    
    // Crear un nuevo servicio
    const servicio = document.createElement('div');
    servicio.classList.add('servicio');
    servicio.innerHTML = `
        <h3>${nombre}</h3>
        <p><strong>Categoría:</strong> ${categoria}</p>
        <p>${descripcion}</p>
    `;
    
    // Añadir el servicio a la lista
    document.getElementById('servicios-lista').appendChild(servicio);
    
    // Limpiar el formulario
    document.getElementById('servicio-form').reset();
});