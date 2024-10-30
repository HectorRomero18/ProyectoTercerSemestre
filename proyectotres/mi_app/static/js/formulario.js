function showAlert() {
    const nombre = document.getElementById('nombre').value;  // Obtener el valor del nombre
    const apellido = document.getElementById('apellido').value;  // Obtener el valor del apellido

    Swal.fire({  // Mostrar la alerta de SweetAlert
        title: '¿Estás seguro?',
        text: `¿Quieres registrar a ${nombre} ${apellido}?`,  // Texto de la alerta
        icon: 'warning',  // Icono de advertencia
        showCancelButton: true,  // Mostrar botón de cancelar
        confirmButtonText: 'Sí, registrar',  // Texto del botón de confirmar
        cancelButtonText: 'No, cancelar'  // Texto del botón de cancelar
    }).then((result) => {
        if (result.isConfirmed) {
            document.forms[0].submit();  // Enviar el formulario si se confirma
        } else {
            return false;  // No enviar el formulario si se cancela
        }
    });

    return false;  // Evitar el envío inmediato
}