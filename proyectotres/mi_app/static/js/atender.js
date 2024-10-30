function showConfirmAlert(nombre, apellido) {
    console.log(nombre); // Verifica que se recibe el nombre correctamente
    Swal.fire({
        title: '¿Confirmar?',
        text: `¿Estás seguro de que deseas atender a ${nombre} ${apellido}?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, confirmar',
        cancelButtonText: 'No, cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('atender-form').submit(); // Envía el formulario
        }
    });
    return false; // Evita el envío inmediato del formulario
}
