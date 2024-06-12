document.addEventListener('DOMContentLoaded', function() {
    // Функція для завантаження та відображення списку вчителів
    function loadTeachers() {
        fetch('/api/teachers')
            .then(response => response.json())
            .then(teachers => {
                const teachersList = document.getElementById('teachers-list');
                // Очищаємо список перед додаванням нових даних
                teachersList.innerHTML = '';
                teachers.forEach(teacher => {
                    const row = teachersList.insertRow();
                    row.innerHTML = `
                        <td>${teacher.id}</td>
                        <td>${teacher.group}</td>
                        <td>${teacher.first_name}</td>
                        <td>${teacher.last_name}</td>
                    `;
                });
            });
    }

    // Викликаємо функцію для ініціалізації списку вчителів
    loadTeachers();

    // EventHandler для форми додавання нового студента
    document.getElementById('teacher-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const id = document.getElementById('id').value;  // Отримуємо ID, якщо воно вказано
        const group = document.getElementById('group').value;
        const firstName = document.getElementById('first_name').value;
        const lastName = document.getElementById('last_name').value;

        const data = {
            id: id,
            group: group,
            first_name: firstName,
            last_name: lastName,
        };

        // Відправляємо дані на сервер для додавання або оновлення вчителя
        fetch('/api/teachers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(() => {
            // Очищаємо форму після додавання вчителя
            document.getElementById('teacher-form').reset();
            // Видаляємо значення ID для уникнення непередбачуваної поведінки
            document.getElementById('id').value = '';
            // Оновлюємо список вчителів на сторінці
            loadTeachers();
        })
        .catch(error => console.error('Error:', error));
    });
});
