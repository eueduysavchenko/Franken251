document.addEventListener('DOMContentLoaded', function() {
    // Функція для завантаження та відображення списку завдань
    function loadNotes() {
        fetch('/api/mark')
            .then(response => response.json())
            .then(notes => {
                const notesList = document.getElementById('notes-list');
                console.log(notesList)
                // Очищаємо список перед додаванням нових даних
                notesList.innerHTML = '';
                notes.forEach(note => {
                    const row = notesList.insertRow();
                    row.innerHTML = `
                        <td>${note.id}</td>
                        <td>${note.name}</td>
                        <td>${note.task}</td>
                        <td>${note.status}</td>
                        <td>${note.date_time}</td>
                    `;
                });
            });
    }

    // Викликаємо функцію для ініціалізації списку записів
    loadNotes();

    // функція додавання даних на сервер
    function addNote(data) {
        fetch('/api/mark', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(() => {
            // Очищаємо форму після додавання запису
            document.getElementById('note-form').reset();
            // Видаляємо значення ID для уникнення непередбачуваної поведінки
            document.getElementById('id').value = '';
            // Оновлюємо список записів на сторінці
            loadNotes();
        })
        .catch(error => console.error('Error:', error));
    }

    // функція видаленняs
    function deleteNote(id) {
        let path = '/api/mark/' + id
        fetch(path, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            loadNotes();
        })
        .catch(error => console.error('Error:', error));
    }

    // EventHandler для форми додавання нового запису
    document.getElementById('note-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const id = document.getElementById('id').value;  // Отримуємо ID
        const name = document.getElementById('name').value;
        const task = document.getElementById('task').value;
        const status = document.getElementById('status').value;
        const date_time = document.getElementById('date_time').value;

        const data = {
            id: id,
            name: name,
            task: task,
            status: status,
            date_time: date_time
        };

        // Відправляємо дані на сервер для додавання або оновлення запис
        addNote(data);
    });

    document.getElementById('note-form-delete').addEventListener('submit', function(event) {
        event.preventDefault();

        note_id = document.getElementById('note_id').value;

        note_id = (note_id < 1) ? (note_id * -1) : note_id // на випадок відʼємних значень

        // Видалення по id
        deleteNote(note_id);
    });
});