document.addEventListener('DOMContentLoaded', function() {
    function deleteStudent(studentId){
        // Відправляємо запит DELETE на сервер для видалення студента за його ID
        fetch(`/api/students/${studentId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(() => {
            // Оновлюємо список студентів на сторінці
            loadStudents();
        })
        .catch(error => console.error('Error:', error));
    }

    function updateStudent(data){
        const loader = document.getElementById('loader');    

        fetch(`/api/students`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)           
        })
        .then(response => response.json())
        .then(() => {
            // Оновлюємо список студентів на сторінці
            loadStudents();            

            // Змінюємо колір кнопки на зелений на 1500 мілісекунди
            const updateButton = document.querySelector(`.update-${data.id}`);
            updateButton.style.backgroundColor = 'lightgreen';
            setTimeout(() => {
                updateButton.style.backgroundColor = ''; // Скидаємо колір на стандартний
            }, 1500);

        })
        .catch(error => console.error('Error:', error));
    }
    
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
                
                console.log(row);
                    row.innerHTML = `
                        <td>${student.id}</td>
                        <td><input class="group" value=${student.group}></td>
                        <td><input class="first_name" value=${student.first_name}></td>
                        <td><input class="last_name" value=${student.last_name}></td>
                        <td><input class="score" value=${student.score}></td>
                        <td>
                            <input class="delete-${student.id}" type="button" value="Delete" data-student-id="${student.id}">
                            <input class="update-${student.id}" type="button" value="Update" data-student-id="${student.id}">                            
                        </td>
                    `;
                     // Додаємо обробник події click до кнопки Delete                    
                    const deleteButton = row.querySelector(`.delete-${student.id}`);
                    deleteButton.addEventListener('click', function() {
                        const studentId = this.getAttribute('data-student-id');
                        deleteStudent(studentId);
                    });

                    // Додаємо обробник події click до кнопки Update
                    const updateButton = row.querySelector(`.update-${student.id}`);
                    updateButton.addEventListener('click', function(event) {
                        const id = this.getAttribute('data-student-id');
                        const group = event.target.parentNode.parentNode.querySelector('.group').value;
                        const firstName = event.target.parentNode.parentNode.querySelector('.first_name').value;
                        const lastName = event.target.parentNode.parentNode.querySelector('.last_name').value;
                        const score = event.target.parentNode.parentNode.querySelector('.score').value;
                        
                        const updatedStudent = {
                            id: id,
                            group: group,
                            first_name: firstName,
                            last_name: lastName,
                            score: score                
                        };                    

                        updateStudent(updatedStudent);                        
                    });
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
