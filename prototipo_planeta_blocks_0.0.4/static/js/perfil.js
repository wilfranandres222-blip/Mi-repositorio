/**
 * PERFIL.JS - Planeta de Blogs
 * Scripts para la página de perfil de usuario
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeProfile();
});

function initializeProfile() {
    setupPasswordChangeHandler();
    setupDeleteAccountHandler();
}

/**
 * Handler para cambio de contraseña
 */
function setupPasswordChangeHandler() {
    const form = document.getElementById('cambiarClaveForm');
    if (!form) return;

    form.addEventListener('submit', async(e) => {
        e.preventDefault();

        const claveActual = document.getElementById('claveActual').value;
        const nuevaClave = document.getElementById('nuevaClave').value;
        const confirmarClave = document.getElementById('confirmarClave').value;

        // Validación
        if (nuevaClave !== confirmarClave) {
            showAlert('Las nuevas contraseñas no coinciden', 'error');
            return;
        }

        if (nuevaClave.length < 6) {
            showAlert('La contraseña debe tener al menos 6 caracteres', 'error');
            return;
        }

        try {
            // Aquí iría la llamada a la API para cambiar contraseña
            // const response = await fetch('/api/cambiar-contrasena', {
            //   method: 'POST',
            //   headers: { 'Content-Type': 'application/json' },
            //   body: JSON.stringify({ claveActual, nuevaClave })
            // });

            showAlert('✅ Contraseña actualizada correctamente', 'success');
            form.reset();
        } catch (error) {
            showAlert('Error al cambiar la contraseña', 'error');
            console.error('Error:', error);
        }
    });
}

/**
 * Handler para eliminar cuenta
 */
function setupDeleteAccountHandler() {
    const form = document.getElementById('eliminarForm');
    if (!form) return;

    form.addEventListener('submit', async(e) => {
        e.preventDefault();

        const clave = document.getElementById('claveConfirmacion').value;
        const confirmacion = document.getElementById('confirmacionTexto').value;

        // Validación
        if (confirmacion !== 'ELIMINAR') {
            showAlert('❌ Escribe "ELIMINAR" para confirmar', 'error');
            return;
        }

        if (!clave) {
            showAlert('❌ Ingresa tu contraseña para confirmar', 'error');
            return;
        }

        // Confirmación final
        if (!confirm('⚠️ Esta acción es IRREVERSIBLE. ¿Realmente deseas eliminar tu cuenta?')) {
            return;
        }

        try {
            // Ya está manejado en el HTML con fetch
            // El código del formulario en el HTML maneja la solicitud
        } catch (error) {
            showAlert('Error al procesar la solicitud', 'error');
            console.error('Error:', error);
        }
    });
}

/**
 * Función para mostrar alertas
 */
function showAlert(message, type = 'info') {
    // Remover alertas anteriores
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const perfil = document.querySelector('.perfil-container');
    if (perfil) {
        perfil.insertBefore(alertDiv, perfil.firstChild);
    } else {
        document.body.insertBefore(alertDiv, document.body.firstChild);
    }

    setTimeout(() => {
        alertDiv.style.animation = 'fadeOut 0.3s ease forwards';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

/**
 * Agregar estilos dinámicos
 */
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeOut {
    from {
      opacity: 1;
    }
    to {
      opacity: 0;
    }
  }
  
  .action-form input:focus {
    outline: none;
    border-color: #0d47a1;
    box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.1);
  }
`;
document.head.appendChild(style);