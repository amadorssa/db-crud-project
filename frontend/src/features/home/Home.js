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

// **¡AÑADE ESTO!**
document.addEventListener('DOMContentLoaded', () => {
  fetchPracticasCount();
});
