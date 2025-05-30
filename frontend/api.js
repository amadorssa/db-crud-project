// frontend/api.js
export const API_BASE = 'http://localhost:8000';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  const text = await res.text();          // Puede venir vacío (204)
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const message = data?.detail || res.statusText || 'Error en la petición';
    throw new Error(message);
  }
  return data;
}

export const API_ENDPOINTS = {
  USERS: {
    CREATE:  '/users/',
    GET_ALL: '/users/',
    GET:     (id) => `/users/${id}/`,
    UPDATE:  (id) => `/users/${id}/`,
    DELETE:  (id) => `/users/${id}/`,
  },
};

export const api = {
  get:    (path)            => request(path, { method: 'GET' }),
  post:   (path, body)      => request(path, { method: 'POST',   body: JSON.stringify(body) }),
  put:    (path, body)      => request(path, { method: 'PUT',    body: JSON.stringify(body) }),
  delete: (path, body=null) => request(path, {
                                   method: 'DELETE',
                                   ...(body ? { body: JSON.stringify(body) } : {}),
                                 }),
};
