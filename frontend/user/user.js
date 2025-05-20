// frontend/user/user.py
import { api, API_ENDPOINTS } from '../api.js';

const successEl = document.getElementById('successMessage');
const errorEl   = document.getElementById('errorMessage');
function showSuccess(msg) {
  successEl.textContent = msg;
  errorEl.textContent = '';
}
function showError(msg) {
  errorEl.textContent = msg;
  successEl.textContent = '';
}

// ==============================
// 1) Crear usuario
// ==============================
document.getElementById('createUserForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const form = e.target;
    const payload = {
      expediente_id: form.expediente_id.value,
      nombre:        form.nombre.value,
      primer_apellido: form.primer_apellido.value,
      segundo_apellido: form.segundo_apellido.value || null,
      email:         form.email.value,
      contrasena:    form.contrasena.value,
      es_admin:      form.es_admin.value === 'true',
      es_activo:     form.es_activo.value === 'true',
    };
    try {
      const response = await api.post(API_ENDPOINTS.USERS.CREATE, payload);
      showSuccess(`Usuario creado con ID ${response.data.usuario_id}`);
      form.reset();
      loadUsers();
    } catch (error) {
      showError(error.response?.data?.detail || error.message || 'Error creando usuario');
    }
  });

// ==============================
// 2) Listar usuarios
// ==============================
async function loadUsers() {
  try {
    const data = await api.get(API_ENDPOINTS.USERS.GET_ALL);
    const tbody = document.getElementById('usersTableBody');
    tbody.innerHTML = '';
    data.forEach(user => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${user.usuario_id}</td>
        <td>${user.expediente_id}</td>
        <td>${user.nombre} ${user.primer_apellido} ${user.segundo_apellido || ''}</td>
        <td>${user.email}</td>
        <td>${user.es_admin}</td>
        <td>${user.es_activo}</td>
        <td>
          <button data-id="${user.usuario_id}" class="btn-detail">Detalles</button>
          <button data-id="${user.usuario_id}" class="btn-load">Cargar</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    showError('No se pudo cargar la lista de usuarios');
  }
}
document.getElementById('refreshList')
  .addEventListener('click', loadUsers);
//Carga inicial
loadUsers();

// ==============================
// 3) Ver detalles de un usuario
// ==============================
document.getElementById('getUserDetails')
  .addEventListener('click', async () => {
    const id = document.getElementById('userId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      const data = await api.get(API_ENDPOINTS.USERS.GET(id));
      document.getElementById('userDetails').innerHTML = `
        <pre>${JSON.stringify(data, null, 2)}</pre>
      `;
      showSuccess('Detalles cargados');
    } catch (error) {
      showError(error.response?.data?.detail || 'Usuario no encontrado');
    }
  });

// ==============================
// 4) Cargar datos para actualizar
// ==============================
document.getElementById('loadUserForUpdate')
  .addEventListener('click', async () => {
    const id = document.getElementById('updateUserId').value;
    if (!id) return showError('Ingresa un ID válido');
    try {
      console.log('Cargando usuario para actualizar', id);
      const data = await api.get(API_ENDPOINTS.USERS.GET(id));
      console.log('Datos del usuario', data);
      document.getElementById('update_expediente_id').value = data.expediente_id;
      document.getElementById('update_nombre').value        = data.nombre;
      document.getElementById('update_primer_apellido').value = data.primer_apellido;
      document.getElementById('update_segundo_apellido').value = data.segundo_apellido || '';
      document.getElementById('update_email').value         = data.email;
      document.getElementById('update_contrasena').value    = data.contrasena;
      document.getElementById('update_es_admin').value      = data.es_admin;
      document.getElementById('update_es_activo').value     = data.es_activo;
      console.log('Datos cargados para actualizar', data);
      showSuccess('Datos cargados para actualizar');
    } catch (error) {
      showError(error.response?.detail || 'Usuario no encontrado');
    }
  });

// ==============================
// 5) Actualizar usuario
// ==============================
document.getElementById('updateUserForm')
  .addEventListener('submit', async e => {
    e.preventDefault();
    const id = document.getElementById('updateUserId').value;
    const payload = {};
    ['expediente_id','nombre','primer_apellido','segundo_apellido','email','contrasena']
      .forEach(f => {
        const v = document.getElementById(`update_${f}`).value;
        if (v) payload[f] = f === 'contrasena' && v === '' ? undefined : v;
      });
    payload.es_admin  = document.getElementById('update_es_admin').value === 'true';
    payload.es_activo = document.getElementById('update_es_activo').value === 'true';
    try {
      await api.put(API_ENDPOINTS.USERS.UPDATE(id), payload);
      showSuccess('Usuario actualizado');
      loadUsers();
    } catch (error) {
      showError(error.response?.data?.detail || 'Error actualizando');
    }
  });

// ==============================
// 6) Eliminar usuario
// ==============================
document.getElementById('deleteUserBtn')
  .addEventListener('click', async () => {
    const id = document.getElementById('deleteUserId').value;
    if (!id) return showError('Ingresa un ID válido');
    if (!confirm(`Eliminar usuario ${id}?`)) return;
    try {
      await api.delete(API_ENDPOINTS.USERS.DELETE(id));
      showSuccess('Usuario eliminado');
      loadUsers();
    } catch (error) {
      showError(error.response?.detail || 'Error eliminando');
    }
  });