/**
 * AUTH.JS - Planeta de Blogs
 * Scripts para manejo de autenticación (login, registro, recuperación)
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeAuthPage();
});

function initializeAuthPage() {
    // Validación en tiempo real de campos
    setupRealTimeValidation();

    // Manejo de submit
    setupFormHandlers();
}

/**
 * Validación en tiempo real
 */
function setupRealTimeValidation() {
    const inputs = document.querySelectorAll('input, textarea, select');

    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
}

/**
 * Validar un campo específico
 */
function validateField(field) {
    let isValid = true;
    let errorMessage = '';

    // Validación requerida
    if (field.required && !field.value.trim()) {
        isValid = false;
        errorMessage = 'Este campo es requerido';
    }

    // Validación de email
    if (field.type === 'email' && field.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
            isValid = false;
            errorMessage = 'Email inválido';
        }
    }

    // Validación de contraseña mínima
    if (field.type === 'password' && field.value && field.minLength) {
        if (field.value.length < field.minLength) {
            isValid = false;
            errorMessage = `Mínimo ${field.minLength} caracteres`;
        }
    }

    // Aplicar estilos
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }

    // Mostrar mensaje de error
    updateFieldError(field, errorMessage, isValid);

    return isValid;
}

/**
 * Actualizar mensaje de error de campo
 */
function updateFieldError(field, message, isValid) {
    // Remover error anterior si existe
    const existingError = field.parentElement.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }

    // Agregar error nuevo si es necesario
    if (message && !isValid) {
        const errorDiv = document.createElement('small');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
      display: block;
      color: #e74c3c;
      margin-top: 0.25rem;
      font-size: 0.875rem;
    `;
        field.parentElement.appendChild(errorDiv);
    }
}

/**
 * Configurar handlers de form
 */
function setupFormHandlers() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            // No prevenir el comportamiento por defecto aquí
            // Dejar que el form HTML maneje la validación
        });
    });
}

/**
 * Validar todo el formulario
 */
function validateForm(form) {
    const fields = form.querySelectorAll('input, textarea, select');
    let isFormValid = true;

    fields.forEach(field => {
        if (!validateField(field)) {
            isFormValid = false;
        }
    });

    return isFormValid;
}

/**
 * Función para mostrar alertas
 */
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.marginBottom = '1rem';

    // Insertar antes del formulario
    const form = document.querySelector('form');
    if (form) {
        form.parentElement.insertBefore(alertDiv, form);
    } else {
        document.body.insertBefore(alertDiv, document.body.firstChild);
    }

    // Auto-remover
    if (duration > 0) {
        setTimeout(() => {
            alertDiv.style.animation = 'fadeOut 0.3s ease forwards';
            setTimeout(() => alertDiv.remove(), 300);
        }, duration);
    }
}

/**
 * Agregar estilos de validación
 */
const style = document.createElement('style');
style.textContent = `
  input.is-valid,
  textarea.is-valid,
  select.is-valid {
    border-color: #27ae60 !important;
    background-color: #f0fdf4 !important;
  }
  
  input.is-invalid,
  textarea.is-invalid,
  select.is-invalid {
    border-color: #e74c3c !important;
    background-color: #fef2f2 !important;
  }
  
  .field-error {
    animation: slideDown 0.2s ease;
  }
  
  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-5px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes fadeOut {
    from {
      opacity: 1;
      transform: translateY(0);
    }
    to {
      opacity: 0;
      transform: translateY(-10px);
    }
  }
`;
document.head.appendChild(style);