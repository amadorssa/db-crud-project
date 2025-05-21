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
// 1) Crear practica
// ==============================
document.getElementById('createInternshipForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const form = e.target;
    const payload = {
      alumno_id: form.alumno_id.value,
      unidad_id: form.unidad_id.value,
      ano: form.ano.value,
      periodo: form.periodo.value,
      estatus: form.estatus.value,
    };
    try {
      await api.post(API_ENDPOINTS.INTERNSHIPS.CREATE, payload);
      showSuccess(`Practica creada`);
      form.reset();
      loadInternships();
    } catch (error) {
      showError(error.response?.detail || error.message || 'Error creando practica');
    }
  });

// ==============================
// 2) Listar practica
// ==============================
async function loadInternships() {
  try {
    const data = await api.get(API_ENDPOINTS.INTERNSHIPS.GET_ALL);
    const tbody = document.getElementById('internshipsTableBody');
    tbody.innerHTML = '';
    data.forEach(internship => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${internship.practica_id}</td>
        <td>${internship.alumno_id}</td>
        <td>${internship.unidad_id}</td>
        <td>${internship.ano}</td>
        <td>${internship.periodo}</td>
        <td>${internship.estatus}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    showError('No se pudo cargar la lista de practicas');
  }
}
document.getElementById('refreshList')
  .addEventListener('click', loadInternships);
//Carga inicial
loadInternships();

// ==============================
// 3) Ver detalles de una practica
// ==============================
document.getElementById('getInternshipDetails')
  .addEventListener('click', async () => {
    const id = document.getElementById('practicaId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      const data = await api.get(API_ENDPOINTS.INTERNSHIPS.GET(id));
      document.getElementById('internshipDetails').innerHTML = `
        <pre>${JSON.stringify(data, null, 2)}</pre>
      `;
      showSuccess('Detalles cargados');
    } catch (error) {
      showError(error.response?.detail || 'Practica no encontrada');
    }
  });

// ==============================
// 4) Cargar datos para actualizar
// ==============================
document.getElementById('loadInternshipForUpdate')
  .addEventListener('click', async () => {
    const id = document.getElementById('updateInternshipId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      console.log('Cargando practica para actualizar', id);
      const data = await api.get(API_ENDPOINTS.INTERNSHIPS.GET(id));
      console.log('Datos de la practica', data);
      document.getElementById('update_alumno_id').value = data.alumno_id;
      document.getElementById('update_unidad_id').value        = data.unidad_id;
      document.getElementById('update_ano').value = data.ano;
      document.getElementById('update_periodo').value = data.periodo;
      document.getElementById('update_estatus').value         = data.estatus;
      console.log('Datos cargados para actualizar', data);
      showSuccess('Datos cargados para actualizar');
    } catch (error) {
      showError(error.response?.detail || 'Practica no encontrada');
    }
  });

// ==============================
// 5) Actualizar practica
// ==============================
document.getElementById('updateInternshipForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const id = document.getElementById('updateInternshipId').value;
    const payload = {};
    alumno_id = document.getElementById('update_alumno_id').value;
    unidad_id = document.getElementById('update_unidad_id').value;
    ano = document.getElementById('update_ano').value;
    periodo = document.getElementById('update_periodo').value;
    estatus = document.getElementById('update_estatus').value;
    try {
      await api.put(API_ENDPOINTS.INTERNSHIPS.UPDATE(id), payload);
      showSuccess('Practica actualizada');
      form.reset();
      loadInternships();
    } catch (error) {
      showError(error.response?.detail || 'Error actualizando');
    }
  });

// ==============================
// 6) Eliminar practica
// ==============================
document.getElementById('deleteInternshipBtn')
  .addEventListener('click', async () => {
    const id = document.getElementById('deleteInternshipId').value;
    if (!id) return showError('Ingresa un ID válido');
    if (!confirm(`Eliminar practica ${id}?`)) return;
    try {
      await api.delete(API_ENDPOINTS.INTERNSHIPS.DELETE(id));
      showSuccess('Practica eliminada');
      form.reset();
      loadInternships();
    } catch (error) {
      showError(error.response?.detail || 'Error eliminando');
    }
  });
