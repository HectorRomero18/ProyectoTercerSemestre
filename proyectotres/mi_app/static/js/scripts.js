function toggleDropdown() {
    const dropdown = document.getElementById('dropdown-menu');
    const overlay = document.getElementById('overlay');
    dropdown.classList.toggle('show');
    overlay.classList.toggle('show');
}
document.addEventListener('click', (event) => {
    const dropdown = document.getElementById('dropdown-menu');
    const overlay = document.getElementById('overlay');
    if (!event.target.closest('button')) {
        dropdown.classList.remove('show');
        overlay.classList.remove('show');
    }
});

function showDeleteAlert(nombre, id) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: `Quieres eliminar a ${nombre}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const response = await fetch(`/eliminar-persona/${id}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                        // No se incluye el CSRF token
                    },
                    body: JSON.stringify({}) // Puedes incluir datos si es necesario
                });

                if (response.ok) {
                    Swal.fire('Eliminado!', `${nombre} ha sido eliminado.`, 'success')
                        .then(() => {
                            location.reload(); // Recarga la página o redirige
                        });
                } else {
                    Swal.fire('Error!', 'No se pudo eliminar la persona.', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                Swal.fire('Error!', 'Ocurrió un error al eliminar.', 'error');
            }
        }
    });
}





function checkAttended(atendido, nombre) {
    if (atendido) {
        Swal.fire({
            title: 'Atendido',
            text: `${nombre} ya ha sido atendido.`,
            icon: 'info',
            confirmButtonText: 'Aceptar'
});
event.preventDefault();
}
}
