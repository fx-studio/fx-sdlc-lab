// A todo has: id, title, done, createdAt. No due date, no tags, no owner.
let todos = store.load();
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
  store.save(todos);
  render();
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
  $('#count').textContent = `${open} việc chưa xong`;
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

render();
