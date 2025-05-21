import { api, API_ENDPOINTS } from '../../../api.js';

export async function fetchPracticasCount() {
  const tableBody = document.getElementById('practicasCountBody');
  if (!tableBody) return;

  tableBody.innerHTML = '<tr><td colspan="2">Cargando datos...</td></tr>';
  try {
    const data = await api.get(API_ENDPOINTS.HOME.GET);
    tableBody.innerHTML = '';
    if (!data.length) {
      tableBody.innerHTML =
        '<tr><td colspan="2">No hay datos de prácticas disponibles.</td></tr>';
      return;
    }
    data.forEach(({ tipo_unidad, cantidad_practicas }) => {
      const row = tableBody.insertRow();
      row.insertCell().textContent = tipo_unidad || 'N/A';
      row.insertCell().textContent = cantidad_practicas;
    });
  } catch (err) {
    console.error(err);
    tableBody.innerHTML =
      `<tr><td colspan="2">Error al cargar los datos: ${err.message}</td></tr>`;
  }
}

export async function fetchEstatusCount() {
  const tableBody = document.getElementById('estatusCountBody');
  if (!tableBody) return;

  tableBody.innerHTML = '<tr><td colspan="2">Cargando datos...</td></tr>';
  try {
      const data = await api.get('/stats/status');
      if (!data.length) {
          tableBody.innerHTML = '<tr><td colspan="2">No hay datos de estatus disponibles.</td></tr>';
          return;
      }
    tableBody.innerHTML = '';
    data.forEach(({ estatus, cantidad_practicas }) => {
      const row = tableBody.insertRow();
      row.insertCell().textContent = estatus || 'N/A';
      row.insertCell().textContent = cantidad_practicas;
    });
  } catch (err) {
    console.error(err);
    tableBody.innerHTML = `<tr><td colspan="2">Error: ${err.message}</td></tr>`;
  }
}

export async function fetchDocumentosCount() {
  const tableBody = document.getElementById('documentosCountBody');
  if (!tableBody) return;

  tableBody.innerHTML = '<tr><td colspan="2">Cargando datos...</td></tr>';
  try {
      const data = await api.get('/stats/documents');
      if (!data.length) {
          tableBody.innerHTML = '<tr><td colspan="2">No hay datos de estatus disponibles.</td></tr>';
          return;
      }
      
    tableBody.innerHTML = '';
    data.forEach(({ tipo_documento, cantidad_documentos }) => {
      const row = tableBody.insertRow();
      row.insertCell().textContent = tipo_documento || 'N/A';
      row.insertCell().textContent = cantidad_documentos;
    });
  } catch (err) {
    console.error(err);
    tableBody.innerHTML = `<tr><td colspan="2">Error: ${err.message}</td></tr>`;
  }
}


export async function fetchReportesCount() {
  const tableBody = document.getElementById('reportesCountBody');
  if (!tableBody) return;

  tableBody.innerHTML = '<tr><td colspan="2">Cargando datos...</td></tr>';
  try {
      const data = await api.get('/stats/reports');
      if (!data.length) {
          tableBody.innerHTML = '<tr><td colspan="2">No hay datos de estatus disponibles.</td></tr>';
          return;
      }
    tableBody.innerHTML = '';
    data.forEach(({ tipo_reporte, cantidad_reportes }) => {
      const row = tableBody.insertRow();
      row.insertCell().textContent = tipo_reporte || 'N/A';
      row.insertCell().textContent = cantidad_reportes;
    });
  } catch (err) {
    console.error(err);
    tableBody.innerHTML = `<tr><td colspan="2">Error: ${err.message}</td></tr>`;
  }
}

export async function fetchAlumnosCount() {
  const tableBody = document.getElementById('alumnosCountBody');
  if (!tableBody) return;

  tableBody.innerHTML = '<tr><td colspan="2">Cargando datos...</td></tr>';
  try {
      const data = await api.get('/stats/users');
      if (!data.length) {
          tableBody.innerHTML = '<tr><td colspan="2">No hay datos de estatus disponibles.</td></tr>';
          return;
      }
    tableBody.innerHTML = '';
    data.forEach(({ nombre_completo, cantidad_practicas }) => {
      const row = tableBody.insertRow();
      row.insertCell().textContent = nombre_completo || 'N/A';
      row.insertCell().textContent = cantidad_practicas;
    });
  } catch (err) {
    console.error(err);
    tableBody.innerHTML = `<tr><td colspan="2">Error: ${err.message}</td></tr>`;
  }
}

// **¡AÑADE ESTO!**
document.addEventListener('DOMContentLoaded', () => {
    fetchPracticasCount();
    fetchEstatusCount();
    fetchDocumentosCount();
    fetchReportesCount();
    fetchAlumnosCount();
});
