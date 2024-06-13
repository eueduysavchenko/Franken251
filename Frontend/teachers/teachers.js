document.addEventListener('DOMContentLoaded', function() {
<<<<<<< HEAD:Frontend/teachers/teachers.js
    // Функція для завантаження та відображення списку вчителів
    function loadTeachers() {
        fetch('/api/teachers')
=======
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
>>>>>>> main:Frontend/students/students.js
            .then(response => response.json())
            .then(teachers => {
                const teachersList = document.getElementById('teachers-list');
                // Очищаємо список перед додаванням нових даних
<<<<<<< HEAD:Frontend/teachers/teachers.js
                teachersList.innerHTML = '';
                teachers.forEach(teacher => {
                    const row = teachersList.insertRow();
                    row.innerHTML = `
                        <td>${teacher.id}</td>
                        <td>${teacher.group}</td>
                        <td>${teacher.first_name}</td>
                        <td>${teacher.last_name}</td>
=======
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
>>>>>>> main:Frontend/students/students.js
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
