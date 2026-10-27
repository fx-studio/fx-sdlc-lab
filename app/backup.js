// Backup to a file and import it back. No DOM and no browser storage here: storage goes through the `store` passed in,
// so this file can be tested in Node. A backup file is { version: 1, todos: [{ id, title, done, createdAt }] }.
const MAX_IMPORT_BYTES = 1048576; // 1 MiB, policy-security#S1. Also the size above which a backup cannot be imported back.

const MESSAGES = {
  nothingToBackUp: 'Chưa có việc nào để sao lưu.',
  backupTooBig: 'File sao lưu đã lưu, nhưng quá lớn nên app không nhập lại được.',
  notSaved: 'Thay đổi vừa rồi chưa được lưu. Hãy sao lưu ra file, rồi xoá bớt việc đã xong.',
  // One sentence for both cases: the list on screen may already hold changes that an earlier failed save left unsaved.
  importNotSaved:
    'Chưa nhập được file. Danh sách trên màn hình vẫn nguyên nhưng có thể chưa được lưu, nên đừng tải lại trang. ' +
    'Hãy sao lưu ra file, xoá bớt việc đã xong rồi thử lại.',
  backedUp: 'Đã sao lưu {n} việc.',
  imported: 'Đã nhập {n} việc.',
  confirmReplace: 'Thay {n} việc hiện có bằng {m} việc trong file?',
  confirmReplaceUnreadable: 'Thay danh sách đã lưu không đọc được bằng {m} việc trong file?',
  confirmReplaceUnreadableAndUnsaved:
    'Thay danh sách đã lưu không đọc được và {n} việc bạn vừa thêm (chưa lưu) bằng {m} việc trong file?',
  emptyFile: 'File này không có việc nào, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu khác.',
  notBackup:
    'File này không phải file sao lưu của app, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. ' +
    'Hãy chọn file tạo từ nút "Sao lưu ra file".',
  badTodo:
    'File sao lưu này bị lỗi, nên chưa nhập được việc nào. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu khác.',
  fileTooBig:
    'File này quá lớn, nên chưa nhập được. Danh sách của bạn vẫn giữ nguyên. Hãy chọn file sao lưu của danh sách ngắn hơn.',
  emptyList: 'Chưa có việc nào. Nếu có file sao lưu, hãy bấm "Nhập từ file".',
  cannotReadFile: 'Không đọc được file này. Danh sách của bạn vẫn giữ nguyên. Hãy chọn lại file hoặc chọn file khác.',
  reading: 'Đang đọc file…',
  unreadable:
    'Không đọc được danh sách đã lưu trên trình duyệt này. Việc bạn thêm hoặc sửa lúc này sẽ không được lưu. ' +
    'Nếu có file sao lưu, hãy bấm "Nhập từ file".',
};

const TODO_KEYS = ['id', 'title', 'done', 'createdAt'];
const FILE_KEYS = ['version', 'todos'];

// Counts in app sentences: a dot every three digits from 1,000 up (1.000, 2.001, 12.500), plain below (999).
// Not for years or dates, which never go through fill().
function formatCount(n) {
  return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

function fill(template, values) {
  return template.replace(/\{(\w+)\}/g, (_, k) => formatCount(values[k]));
}

function pick(t) {
  return { id: t.id, title: t.title, done: t.done, createdAt: t.createdAt };
}

function isObject(v) {
  return v !== null && typeof v === 'object' && !Array.isArray(v);
}

function hasExactKeys(o, keys) {
  const own = Object.keys(o);
  return own.length === keys.length && keys.every((k) => Object.prototype.hasOwnProperty.call(o, k));
}

function isValidTodo(t) {
  return (
    isObject(t) &&
    hasExactKeys(t, TODO_KEYS) &&
    typeof t.id === 'string' && t.id !== '' &&
    typeof t.title === 'string' && t.title.trim() !== '' &&
    typeof t.done === 'boolean' &&
    typeof t.createdAt === 'number' && Number.isFinite(t.createdAt)
  );
}

function toBackupText(todos) {
  return JSON.stringify({ version: 1, todos: todos.map(pick) }, null, 2);
}

// The customer's own day (local time), not UTC.
function backupFileName(date) {
  const pad = (n) => String(n).padStart(2, '0');
  return `todo-sao-luu-${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}.json`;
}

function tooBigToImport(text) {
  return new TextEncoder().encode(text).length > MAX_IMPORT_BYTES;
}

// Untrusted input: only JSON.parse, never evaluated. Rejects the whole file on any bad todo (no partial import).
function parseBackup(text) {
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    return { ok: false, message: MESSAGES.notBackup };
  }
  if (!isObject(data) || !hasExactKeys(data, FILE_KEYS) || data.version !== 1 || !Array.isArray(data.todos)) {
    return { ok: false, message: MESSAGES.notBackup };
  }
  if (data.todos.length === 0) return { ok: false, message: MESSAGES.emptyFile };
  const ids = new Set();
  for (const t of data.todos) {
    if (!isValidTodo(t) || ids.has(t.id)) return { ok: false, message: MESSAGES.badTodo };
    ids.add(t.id);
  }
  return { ok: true, todos: data.todos.map(pick) };
}

// null when nothing would be lost (empty list, saved list readable), so no confirmation is needed.
function confirmText({ readError, current, incoming }) {
  if (readError && current === 0) return fill(MESSAGES.confirmReplaceUnreadable, { m: incoming });
  if (readError) return fill(MESSAGES.confirmReplaceUnreadableAndUnsaved, { n: current, m: incoming });
  if (current === 0) return null;
  return fill(MESSAGES.confirmReplace, { n: current, m: incoming });
}

// After add, toggle or remove. 'skipped' (saved list unreadable) shows nothing extra: the banner already says so.
function persist(store, todos) {
  return { message: store.save(todos) === 'failed' ? MESSAGES.notSaved : null };
}

// Returns the list to show and the message. Every path except a successful replace returns `current` unchanged.
// Writes only through store.replace, never store.save, so an unreadable saved list is replaced only here.
async function importBackup({ store, current, file, ask }) {
  const keep = (message) => ({ todos: current, message });
  if (file.size > MAX_IMPORT_BYTES) return keep(MESSAGES.fileTooBig);
  let text;
  try {
    text = await file.text();
  } catch {
    return keep(MESSAGES.cannotReadFile);
  }
  const parsed = parseBackup(text);
  if (!parsed.ok) return keep(parsed.message);
  const question = confirmText({ readError: store.readError, current: current.length, incoming: parsed.todos.length });
  if (question !== null && !(await ask(question))) return keep(null);
  if (store.replace(parsed.todos) !== 'saved') return keep(MESSAGES.importNotSaved);
  return { todos: parsed.todos, message: fill(MESSAGES.imported, { n: parsed.todos.length }) };
}

if (typeof module !== 'undefined') {
  module.exports = {
    MAX_IMPORT_BYTES, MESSAGES, formatCount, fill, toBackupText, backupFileName, tooBigToImport, parseBackup, confirmText, persist,
    importBackup,
  };
}
