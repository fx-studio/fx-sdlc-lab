# Public names (from the tech lead; no code bodies)

Code lives in `../app/` relative to the tests folder. Load Node modules with `require('../app/<file>.js')`. You may not read app/.

## app/backup.js (Node module, no DOM, no browser storage)
- `MAX_IMPORT_BYTES`: number, the import size limit in bytes.
- `MESSAGES`: object of every sentence the customer sees. Keys: nothingToBackUp, backupTooBig, notSaved, backedUp, imported,
  confirmReplace, confirmReplaceUnreadable, confirmReplaceUnreadableAndUnsaved, emptyFile, notBackup, badTodo, fileTooBig,
  emptyList, cannotReadFile, reading, unreadable. Templates use `{n}` (todos now) and `{m}` (todos in the file).
- `fill(template, values)` → string with `{n}`/`{m}` replaced.
- `toBackupText(todos)` → the text of a backup file.
- `backupFileName(date)` → the download file name for that date.
- `tooBigToImport(text)` → boolean, true when that backup text could not be imported back.
- `parseBackup(text)` → `{ ok: true, todos }` or `{ ok: false, message }`.
- `confirmText({ readError, current, incoming })` → the confirm question (string), or `null` when no question is needed.
  `current` and `incoming` are counts.
- `persist(store, todos)` → `{ message }` after add / toggle / remove (message is null when nothing to say).
- `importBackup({ store, current, file, ask })` → Promise of `{ todos, message }`. `current` is the list on screen (array);
  `file` has `size` (bytes) and `text()` (Promise of string); `ask(question)` → Promise of boolean (true = replace).

## app/store.js (Node module; uses global `localStorage`, which you must fake)
- `store.readError`: boolean. `store.load()` → `{ todos, readError }`. `store.save(todos)` and `store.replace(todos)` →
  `'saved' | 'failed' | 'skipped'`. Storage key: `STORE_KEY` (exported).

## app/app.js (page script, no exports)
Runs in the page after store.js and backup.js, using their globals. Element ids in index.html: notices, unreadable, message,
add, title, filters, list, empty, count, backup, export, import-label, import, where-kept, confirm, confirm-text.
