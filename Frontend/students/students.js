document.addEventListener('DOMContentLoaded', function() {
    // Функція для завантаження та відображення списку студентів
    function loadStudents() {
        fetch('/api/students')
            .then(response => response.json())
            .then(students => {
                const studentsList = document.getElementById('students-list');
                // Очищаємо список перед додаванням нових даних
                studentsList.innerHTML = '';
                students.forEach(student => {
                    const row = studentsList.insertRow();
                    row.innerHTML = `
                        <td>${student.id}</td>
                        <td>${student.group}</td>
                        <td>${student.first_name}</td>
                        <td>${student.last_name}</td>
                        <td>${student.score}</td>
                    `;
                });
            });
    }

    // Викликаємо функцію для ініціалізації списку студентів
    loadStudents();

    // EventHandler для форми додавання нового студента
    document.getElementById('student-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const id = document.getElementById('id').value;  // Отримуємо ID, якщо воно вказано
        const group = document.getElementById('group').value;
        const firstName = document.getElementById('first_name').value;
        const lastName = document.getElementById('last_name').value;
        const score = document.getElementById('score').value;

        const data = {
            id: id,
            group: group,
            first_name: firstName,
            last_name: lastName,
            score: score
        };

        // Відправляємо дані на сервер для додавання або оновлення студента
        fetch('/api/students', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(() => {
            // Очищаємо форму після додавання студента
            document.getElementById('student-form').reset();
            // Видаляємо значення ID для уникнення непередбачуваної поведінки
            document.getElementById('id').value = '';
            // Оновлюємо список студентів на сторінці
            loadStudents();
        })
        .catch(error => console.error('Error:', error));
    });
});
