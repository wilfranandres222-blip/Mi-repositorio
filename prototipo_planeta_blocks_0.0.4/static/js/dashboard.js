/**
 * DASHBOARD.JS - Planeta de Blogs
 * Scripts para el dashboard de usuario
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    loadUserBlogs();
    setupEventListeners();
    setupBlogFormHandler();
}

/**
 * Cargar blogs del usuario (dummy data por ahora)
 */
function loadUserBlogs() {
    const blogsGrid = document.getElementById('blogsGrid');

    // Simular blogs del usuario
    const userBlogs = [
        // Aquí irían los blogs reales del usuario desde la API
    ];

    if (userBlogs.length === 0) {
        // Mostrar estado vacío (ya viene en el HTML)
        return;
    }

    blogsGrid.innerHTML = '';
    userBlogs.forEach(blog => {
        const blogCard = createBlogCard(blog);
        blogsGrid.appendChild(blogCard);
    });
}

/**
 * Crear elemento de tarjeta de blog
 */
function createBlogCard(blog) {
    const card = document.createElement('div');
    card.className = 'blog-card';
    card.innerHTML = `
    <h3>${escapeHtml(blog.titulo)}</h3>
    <p>${escapeHtml(blog.resumen)}</p>
    <div class="blog-meta">
      <span>👤 ${escapeHtml(blog.autor)}</span>
      <span>📅 ${formatDate(blog.fecha)}</span>
    </div>
  `;
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => viewBlog(blog.id));
    return card;
}

/**
 * Ver un blog específico
 */
function viewBlog(blogId) {
    console.log('Ver blog:', blogId);
    // Implementar navegación a blog específico
}

/**
 * Escapar HTML para evitar XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Formatear fecha
 */
function formatDate(date) {
    return new Date(date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Setup de event listeners
 */
function setupEventListeners() {
    // El botón de crear blog está en el HTML
}

/**
 * Handler para formulario de crear blog
 */
function setupBlogFormHandler() {
    const form = document.getElementById('blogForm');
    if (!form) return;

    form.addEventListener('submit', async(e) => {
        e.preventDefault();

        const titulo = document.getElementById('blogTitle').value;
        const categoria = document.getElementById('blogCategory').value;
        const contenido = document.getElementById('blogContent').value;

        try {
            // Aquí iría la llamada a la API para crear el blog
            // const response = await fetch('/api/blogs', {
            //   method: 'POST',
            //   headers: { 'Content-Type': 'application/json' },
            //   body: JSON.stringify({ titulo, categoria, contenido })
            // });

            showAlert('✅ Blog publicado con éxito', 'success');
            form.reset();
            document.getElementById('blogModal').style.display = 'none';
            loadUserBlogs();
        } catch (error) {
            showAlert('Error al publicar el blog', 'error');
            console.error('Error:', error);
        }
    });
}

/**
 * Función para mostrar alertas
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const main = document.querySelector('.dashboard-main');
    if (main) {
        main.insertBefore(alertDiv, main.firstChild);
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
`;
document.head.appendChild(style);