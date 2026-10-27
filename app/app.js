// A todo has: id, title, done, createdAt. No due date, no tags, no owner.
// Saving and importing decisions live in backup.js (persist, importBackup); this file only wires them to the page.
let todos = store.load().todos;
let filter = 'all';

const $ = (sel) => document.querySelector(sel);

function add(title) {
  todos.push({ id: crypto.randomUUID(), title: title.trim(), done: false, createdAt: Date.now() });
  commit();
}

function toggle(id) {
  const t = todos.find((x) => x.id === id);
  if (t) t.done = !t.done;
  commit();
}

function remove(id) {
  todos = todos.filter((x) => x.id !== id);
  commit();
}

function commit() {
  show(persist(store, todos).message);
  render();
}

function show(message) {
  $('#message').textContent = message || '';
}

function visible() {
  if (filter === 'open') return todos.filter((t) => !t.done);
  if (filter === 'done') return todos.filter((t) => t.done);
  return todos;
}

function render() {
  const list = $('#list');
  list.innerHTML = '';
  for (const t of visible()) {
    const li = document.createElement('li');
    li.className = t.done ? 'done' : '';
    li.innerHTML = `<label><input type="checkbox" ${t.done ? 'checked' : ''}> <span></span></label><button aria-label="Xoá">×</button>`;
    li.querySelector('span').textContent = t.title;
    li.querySelector('input').onchange = () => toggle(t.id);
    li.querySelector('button').onclick = () => remove(t.id);
    list.append(li);
  }
  const open = todos.filter((t) => !t.done).length;
  $('#count').textContent = `${formatCount(open)} việc chưa xong`;
  $('#unreadable').hidden = !store.readError;
  // Based on the whole list, not the filter; and not shown on a read error, where the list only looks empty.
  $('#empty').hidden = todos.length > 0 || store.readError;
}

// Resolves true only when the customer picks "Thay"; Esc and "Huỷ" resolve false.
function ask(question) {
  const dialog = $('#confirm');
  $('#confirm-text').textContent = question;
  dialog.returnValue = '';
  dialog.showModal();
  return new Promise((resolve) => {
    dialog.addEventListener('close', () => resolve(dialog.returnValue === 'yes'), { once: true });
  });
}

$('#add').onsubmit = (e) => {
  e.preventDefault();
  const input = $('#title');
  if (input.value.trim()) add(input.value);
  input.value = '';
};

$('#filters').onclick = (e) => {
  const f = e.target.dataset.filter;
  if (!f) return;
  filter = f;
  document.querySelectorAll('#filters button').forEach((b) => b.classList.toggle('on', b.dataset.filter === f));
  render();
};

$('#export').onclick = () => {
  if (todos.length === 0) return show(MESSAGES.nothingToBackUp);
  const text = toBackupText(todos);
  const url = URL.createObjectURL(new Blob([text], { type: 'application/json' }));
  const a = document.createElement('a');
  a.href = url;
  a.download = backupFileName(new Date());
  document.body.append(a);
  a.click();
  a.remove();
  // Revoking right after click() can break the download on Safari iOS, so wait.
  setTimeout(() => URL.revokeObjectURL(url), 10000);
  show(tooBigToImport(text) ? MESSAGES.backupTooBig : fill(MESSAGES.backedUp, { n: todos.length }));
};

$('#import').onchange = async (e) => {
  const input = e.target;
  const file = input.files[0];
  input.value = ''; // so the same file can be picked again
  if (!file) return;
  show(MESSAGES.reading);
  // Counted when importBackup decides whether to ask (after the file is read), not now: another import, an add or a
  // delete may change the list while the file is being read. importBackup only reads current.length and returns
  // current itself when nothing was replaced.
  const current = { get length() { return todos.length; } };
  const result = await importBackup({ store, current, file, ask });
  if (result.todos !== current) todos = result.todos;
  show(result.message);
  render();
};

$('#unreadable').textContent = MESSAGES.unreadable;
$('#empty').textContent = MESSAGES.emptyList;
render();
