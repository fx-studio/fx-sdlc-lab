// Storage layer. Everything lives in this browser's localStorage: no server, no account, no sync.
// Clearing site data, switching browser or switching device means starting from an empty list.
const STORE_KEY = 'todo.v1';

const store = {
  load() {
    try {
      return JSON.parse(localStorage.getItem(STORE_KEY)) || [];
    } catch {
      return [];
    }
  },
  save(todos) {
    // localStorage is capped per origin (about 5 MB in most browsers). A failed write is only logged.
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify(todos));
    } catch (err) {
      console.error('save failed', err);
    }
  },
};
