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
// 1) Crear Unidad
// ==============================
document.getElementById('createUnitForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const form = e.target;
    const payload = {
      nombre: form.nombre.value,
      tipo_unidad: form.tipo_unidad.value,
      direccion: form.direccion.value || null,
      ciudad: form.ciudad.value || null,
      estado: form.estado.value || null,
      capacidad: form.capacidad.value ? parseInt(form.capacidad.value) : null,
      nombre_contacto: form.nombre_contacto.value,
      email_contacto: form.email_contacto.value,
      telefono_contacto: form.telefono_contacto.value,
      es_disponible: form.es_disponible.value === 'true',
    };
    try {
      await api.post(API_ENDPOINTS.UNITS.CREATE, payload);
      showSuccess(`Unidad creada`);
      form.reset();
      loadUnits();
    } catch (error) {
      showError(error.response?.detail || error.message || 'Error creando unidad');
    }
  });

// ==============================
// 2) Listar Unidades
// ==============================
async function loadUnits() {
  try {
    const data = await api.get(API_ENDPOINTS.UNITS.GET_ALL);
    const tbody = document.getElementById('unitsTableBody');
    tbody.innerHTML = '';
    data.forEach(unit => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${unit.unidad_id}</td>
        <td>${unit.nombre}</td>
        <td>${unit.tipo_unidad}</td>
        <td>${unit.capacidad}</td>
        <td>${unit.nombre_contacto}</td>
        <td>${unit.es_disponible}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    showError('No se pudo cargar la lista de unidades');
  }
}
document.getElementById('refreshUnitList')
  .addEventListener('click', loadUnits);
//Carga inicial
loadUnits();

// ==============================
// 3) Ver detalles de un usuario
// ==============================
document.getElementById('getUnitDetails')
  .addEventListener('click', async () => {
    const id = document.getElementById('unitId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      const data = await api.get(API_ENDPOINTS.UNITS.GET(id));
      document.getElementById('unitDetails').innerHTML = `
        <pre>${JSON.stringify(data, null, 2)}</pre>
      `;
      showSuccess('Detalles cargados');
    } catch (error) {
      showError(error.response?.detail || 'Unidad no encontrada');
    }
  });

// ==============================
// 4) Cargar datos para actualizar
// ==============================
document.getElementById('loadUnitForUpdate')
  .addEventListener('click', async () => {
    const id = document.getElementById('updateUnitId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      console.log('Cargando unidad para actualizar', id);
      const data = await api.get(API_ENDPOINTS.UNITS.GET(id));
      console.log('Datos de la unidad', data);
      document.getElementById('update_nombre').value = data.nombre;
      document.getElementById('update_tipo_unidad').value        = data.tipo_unidad;
      document.getElementById('update_capacidad').value = data.capacidad || '';
      document.getElementById('update_nombre_contacto').value = data.nombre_contacto;
      document.getElementById('update_email_contacto').value         = data.email_contacto || '';
      document.getElementById('update_telefono_contacto').value    = data.telefono_contacto || '';
      document.getElementById('update_es_disponible').value     = data.es_disponible;
      console.log('Datos cargados para actualizar', data);
      showSuccess('Datos cargados para actualizar');
    } catch (error) {
      showError(error.response?.detail || 'Unidad no encontrada');
    }
  });

// ==============================
// 5) Actualizar unidad
// ==============================
document.getElementById('updateUnitForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const id = document.getElementById('updateUnitId').value;
    const payload = {};
      ['nombre', 'tipo_unidad','capacidad','nombre_contacto','email_contacto','telefono_contacto']
      .forEach(f => {
        const v = document.getElementById(`update_${f}`).value;
        if (v) payload[f] = v === '' ? undefined : v;
      });
    payload.es_disponible  = document.getElementById('update_es_disponible').value === 'true';
    try {
      await api.put(API_ENDPOINTS.UNITS.UPDATE(id), payload);
      showSuccess('Unidad actualizado');
      form.reset();
      loadUnits();
    } catch (error) {
      showError(error.response?.detail || 'Error actualizando');
    }
  });

// ==============================
// 6) Eliminar usuario
// ==============================
document.getElementById('deleteUnitBtn')
  .addEventListener('click', async () => {
    const id = document.getElementById('deleteUnitId').value;
    if (!id) return showError('Ingresa un ID válido');
    if (!confirm(`Eliminar unidad ${id}?`)) return;
    try {
      await api.delete(API_ENDPOINTS.UNITS.DELETE(id));
      showSuccess('Unidad eliminada');
      loadUnits();
    } catch (error) {
      showError(error.response?.detail || 'Error eliminando');
    }
  });
