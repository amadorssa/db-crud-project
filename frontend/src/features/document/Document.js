// frontend/documentos/documentos.js
import { api, API_ENDPOINTS } from '../../../api.js';

const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');
let ruta = "";

function showMessage(element, message, duration = 5000) {
    element.textContent = message;
    element.style.display = 'block';
    setTimeout(() => {
        element.style.display = 'none';
    }, duration);
}

function showError(message) {
    showMessage(errorMessage, message);
}

function showSuccess(message) {
    showMessage(successMessage, message);
}

// ==============================
// 1) Crear documento
// ==============================
document.getElementById('createDocumentForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const form = e.target;
    const payload = {
        "practica_id": form.practica_id.value,
        "tipo_documento": form.tipo_documento.value,
        "ruta": form.ruta.value,
        "es_verificado": form.es_verificado.value === 'true',
        "es_activo": form.es_activo.value === 'true',
    };
    try {
      await api.post(API_ENDPOINTS.DOCUMENTS.CREATE, payload);
      showSuccess(`Documento creado`);
      form.reset();
      loadDocuments();
    } catch (error) {
      showError(error.response?.detail || error.message || 'Error creando documento');
    }
  });

// ==============================
// 2) Listar documentos
// ==============================
async function loadDocuments() {
  try {
    const data = await api.get(API_ENDPOINTS.DOCUMENTS.GET_ALL);
    const tbody = document.getElementById('documentsTableBody');
    tbody.innerHTML = '';
    data.forEach(doc => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${doc.documento_id}</td>
        <td>${doc.practica_id}</td>
        <td>${doc.tipo_documento}</td>
        <td>${doc.ruta}</td>
        <td>${doc.es_verificado}</td>
        <td>${doc.es_activo}</td>
        <td>${doc.creado_el}</td>
        <td>${doc.actualizado_el}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    showError('No se pudo cargar la lista de documentos');
  }
}
document.getElementById('refreshDocuments')
  .addEventListener('click', loadDocuments);
loadDocuments();

// ==============================
// 3) Ver detalles de un documento
// ==============================
document.getElementById('getDocumentDetails')
  .addEventListener('click', async () => {
    const id = document.getElementById('documentId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      const data = await api.get(API_ENDPOINTS.DOCUMENTS.GET(id));
      document.getElementById('documentDetails').innerHTML = `
        <pre>${JSON.stringify(data, null, 2)}</pre>
      `;
      showSuccess('Detalles cargados');
    } catch (error) {
      showError(error.response?.detail || 'Documento no encontrado');
    }
  });

// ==============================
// 4) Cargar datos para actualizar
// ==============================
document.getElementById('loadDocumentForUpdate')
  .addEventListener('click', async () => {
    const id = document.getElementById('updateDocumentId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      const data = await api.get(API_ENDPOINTS.DOCUMENTS.GET(id));
        document.getElementById('update_practica_id').value = data.practica_id;
        document.getElementById('update_tipo_documento').value = data.tipo_documento;
        document.getElementById('update_es_verificado').value = data.es_verificado;
        document.getElementById('update_es_activo').value = data.es_activo;
        ruta = data.ruta;
        
        const archivoInfo = document.getElementById('archivo_actual_info');

      if (data.ruta) {
          archivoInfo.innerHTML = `${data.ruta} Este es el archivo actual`;
      } else {
        archivoInfo.textContent = 'No hay archivo cargado';
      }
        
      showSuccess('Datos cargados para actualizar');
    } catch (error) {
        console.error('Error al cargar datos para actualizar', error);
      showError(error.response?.detail || ' no encontrado');
    }
  });

// ==============================
// 5) Actualizar documento
// ==============================
document.getElementById('updateDocumentForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
      const id = document.getElementById('updateDocumentId').value;
      if (ruta === "") {
        ruta = document.getElementById('update_ruta').value;
      }
    const payload = {
        "practica_id": document.getElementById('update_practica_id').value,
        "tipo_documento": document.getElementById('update_tipo_documento').value,
        "ruta": ruta,
        "es_verificado": document.getElementById('update_es_verificado').value === 'true',
        "es_activo": document.getElementById('update_es_activo').value === 'true'
    };
    try {
      await api.put(API_ENDPOINTS.DOCUMENTS.UPDATE(id), payload);
      showSuccess('Documento actualizado');
        loadDocuments();
        ruta = "";
    } catch (error) {
      showError(error.response?.detail || 'Error actualizando');
    }
  });

// ==============================
// 6) Eliminar documento
// ==============================
document.getElementById('deleteDocumentBtn')
  .addEventListener('click', async () => {
    const id = document.getElementById('deleteDocumentId').value;
    if (!id) return showError('Ingresa un ID válido');
    if (!confirm(`Eliminar documento ${id}?`)) return;
    try {
      await api.delete(API_ENDPOINTS.DOCUMENTS.DELETE(id));
      showSuccess('Documento eliminado');
      loadDocuments();
    } catch (error) {
      showError(error.response?.detail || 'Error eliminando');
    }
  });
