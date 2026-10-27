// Storage layer. Everything lives in this browser's localStorage: no server, no account, no sync.
// Clearing site data, switching browser or switching device means starting from an empty list.
const STORE_KEY = 'todo.v1';

const store = {
  // True when todo.v1 holds something that cannot be read as a list. Kept in page memory only. While it is true, save()
  // never writes, so the unreadable data is not overwritten; only replace() (import, after the customer agreed) may.
  readError: false,

  // No key yet is an ordinary empty list. Unparsable data, data that is not an array, or storage that throws is a read error.
  load() {
    let todos = null;
    try {
      const raw = localStorage.getItem(STORE_KEY);
      todos = raw === null ? [] : JSON.parse(raw);
    } catch {
      todos = null;
    }
    store.readError = !Array.isArray(todos);
    return { todos: store.readError ? [] : todos, readError: store.readError };
  },

  // 'saved' | 'failed' (for example storage full, about 5 MB in most browsers) | 'skipped' (read error, nothing written).
  save(todos) {
    if (store.readError) return 'skipped';
    return writeList(todos);
  },

  // The import path: writes even after a read error, and clears it only when the write succeeds.
  replace(todos) {
    const result = writeList(todos);
    if (result === 'saved') store.readError = false;
    return result;
  },
};

function writeList(todos) {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify(todos));
    return 'saved';
  } catch {
    return 'failed';
  }
}

if (typeof module !== 'undefined') module.exports = { store, STORE_KEY };
