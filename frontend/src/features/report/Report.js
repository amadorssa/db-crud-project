// frontend/user/user.py
import { api, API_ENDPOINTS } from '../../../api.js';

const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');

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
// 1) Crear reporte
// ==============================
document.getElementById('createReportForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const form = e.target;
    const payload = {
      alumno_id: form.alumno_id.value,
      practica_id: form.practica_id.value,
      fecha: form.fecha.value,
      unidad: form.unidad.value,
      tipo_reporte: form.tipo_reporte.value,
      descripcion: form.descripcion.value,
      evidencia: form.evidencia.value || null,
      anonimo: form.anonimo.value,
      es_abierto: form.es_abierto.value === 'true',
    };
    try {
      await api.post(API_ENDPOINTS.REPORTS.CREATE, payload);
      showSuccess(`Reporte creado`);
      form.reset();
      loadUsers();
    } catch (error) {
      showError(error.response?.detail || error.message || 'Error creando reporte');
    }
  });

// ==============================
// 2) Listar reportes
// ==============================
async function loadReports() {
  try {
    const data = await api.get(API_ENDPOINTS.REPORTS.GET_ALL);
    const tbody = document.getElementById('reportsTableBody');
    tbody.innerHTML = '';
    data.forEach(report => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${report.reporte_id}</td>
        <td>${report.practica_id}</td>
        <td>${report.fecha}</td>
        <td>${report.unidad}</td>
        <td>${report.tipo_reporte}</td>
        <td>${report.anonimo}</td>
        <td>${report.es_abierto}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    showError('No se pudo cargar la lista de usuarios');
  }
}
document.getElementById('refreshList')
  .addEventListener('click', loadReports);
//Carga inicial
loadReports();

// ==============================
// 3) Ver detalles de un reporte
// ==============================
document.getElementById('getReportDetails')
  .addEventListener('click', async () => {
    const id = document.getElementById('reportId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      const data = await api.get(API_ENDPOINTS.REPORTS.GET(id));
      document.getElementById('reportDetails').innerHTML = `
        <pre>${JSON.stringify(data, null, 2)}</pre>
      `;
      showSuccess('Detalles cargados');
    } catch (error) {
      showError(error.response?.detail || 'Reporte no encontrado');
    }
  });

// ==============================
// 4) Cargar datos para actualizar
// ==============================
document.getElementById('loadReportForUpdate')
  .addEventListener('click', async () => {
    const id = document.getElementById('updateReportId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      console.log('Cargando reporte para actualizar', id);
      const data = await api.get(API_ENDPOINTS.REPORTS.GET(id));
      console.log('Datos del reporte', data);
      document.getElementById('update_fecha').value = data.fecha;
      document.getElementById('update_tipo_reporte').value = data.tipo_reporte;
      document.getElementById('update_descripcion').value = data.descripcion;
      document.getElementById('update_evidencia').value = data.evidencia || '';
      document.getElementById('update_anonimo').value = data.anonimo;
      document.getElementById('update_es_abierto').value = data.es_abierto;
      console.log('Datos cargados para actualizar', data);
      showSuccess('Datos cargados para actualizar');
    } catch (error) {
      showError(error.response?.detail || 'Reporte no encontrado');
    }
  });

// ==============================
// 5) Actualizar Reporte
// ==============================
document.getElementById('updateReportForm')
  .addEventListener('submit', async e => {  
    e.preventDefault();
    const id = document.getElementById('updateReportId').value;
    const payload = {};
    ['fecha','tipo_reporte','descripcion','evidencia','anonimo','es_abierto']
      .forEach(f => {
        const v = document.getElementById(`update_${f}`).value;
        if (v) payload[f] = v === '' ? undefined : v;
      });

    // Tratamiento especial para evidencia (permitir vacío = null)
    const evidencia = document.getElementById('update_evidencia').value;
    payload['evidencia'] = evidencia.trim() === '' ? null : evidencia;
    
    try {
      await api.put(API_ENDPOINTS.REPORTS.UPDATE(id), payload);
      showSuccess('Reporte actualizado');
      loadReports();
    } catch (error) {
      showError(error.response?.detail || 'Error actualizando');
    }
  });

// ==============================
// 6) Eliminar reporte
// ==============================
document.getElementById('deleteReportBtn')
  .addEventListener('click', async () => {
    const id = document.getElementById('deleteReportId').value;
    if (!id) return showError('Ingresa un ID válido');
    if (!confirm(`Eliminar Reporte ${id}?`)) return;
    try {
      await api.delete(API_ENDPOINTS.REPORTS.DELETE(id));
      showSuccess('Reporte eliminado');
      loadReports();
    } catch (error) {
      showError(error.response?.detail || 'Error eliminando');
    }
  });
