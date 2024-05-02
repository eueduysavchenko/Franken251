function createButton(text, onClickFunction) {
    const button = document.createElement('button');
    button.type = 'button';
    button.innerText = text;
    button.onclick = onClickFunction;
    button.id = 'add-update-form-button'
    return button;
}

function setupAddButton() {
    const buttonContainer = document.getElementById('add-update-button-container');
    buttonContainer.innerHTML = ''; // Clear any existing content
    const addButton = createButton('Add', submitForm);
    buttonContainer.appendChild(addButton);
}

function setupUpdateButton() {
    const buttonContainer = document.getElementById('add-update-button-container');
    buttonContainer.innerHTML = ''; // Clear any existing content
    const updateButton = createButton('Update', submitForm);
    buttonContainer.appendChild(updateButton);
}

function submitForm() {
    const id = document.getElementById('task-id').value;  // Отримуємо ID, якщо воно вказано
    const person = document.getElementById('person').value;
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const status = document.getElementById('status').value;

    const data = {
        id: id,
        person: person,
        title: title,
        description: description,
        status: status
    };
    if (id) {
        updateTask(id, data);
    } else {
        addTask(data);
    }
}

function addTask(data) {
    console.log('Adding task:', data);
    // Відправляємо дані на сервер для додавання завдання
    fetch('/api/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        resetAddUpdateForm();
        // Оновлюємо список студентів на сторінці
        loadTasksTable();
    })
    .catch(error => console.error('Error:', error));
}

function updateTask(task_id, data) {
    console.log('Updating task:', task_id, data);
        // Відправляємо дані на сервер для додавання завдання
    fetch(`/api/tasks/update/${task_id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        resetAddUpdateForm();
        loadTasksTable();
    })
    .catch(error => console.error('Error:', error));
}

function loadUpdateForm(task_id) {
    console.log('Loading task data to update:', task_id);
    fetch(`/api/tasks/${task_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Task not found');
            }
            return response.json();
        })
        .then(task => {
            document.getElementById('task-id').value = task.id;
            document.getElementById('person').value = task.person;
            document.getElementById('title').value = task.title;
            document.getElementById('description').value = task.description;
            document.getElementById('status').value = task.status;

            setupFormTitle(false);
            setupUpdateButton(); // Change button to 'Update'
        })
        .catch(error => console.error('Error:', error));
}

function deleteTask(task_id) {
    fetch(`/api/tasks/delete/${task_id}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                // Оновлюємо список студентів на сторінці
                loadTasksTable();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}

function loadTasksTable() {
    fetch('/api/tasks')
        .then(response => response.json())
        .then(tasks => {
            const tasksList = document.getElementById('tasks-list');
            // Очищаємо список перед додаванням нових даних
            tasksList.innerHTML = '';
            tasks.forEach(task => {
                const row = tasksList.insertRow();
                row.innerHTML = `
                    <td>${task.id}</td>
                    <td>${task.person}</td>
                    <td>${task.title}</td>
                    <td>${task.description}</td>
                    <td>${task.status}</td>
                    <td class="table-button-cell">
                        <button class="table-button delete-task-button" onclick="deleteTask(${task.id})">❌</button>
                        <button class="table-button update-task-button" onclick="loadUpdateForm(${task.id})">✍️</button>
                    </td>
                `;
            });
        });
}

function resetAddUpdateForm() {
    setupFormTitle();
    setupAddButton();
    // Очищаємо форму після додавання студента
    document.getElementById('task-form').reset();
    // Видаляємо значення ID для уникнення непередбачуваної поведінки
    document.getElementById('task-id').value = '';
    validateForm();
}

function setupFormTitle(isAddTask = true) {
    document.getElementById('form-title').innerText = isAddTask ? "Add Task" : "Update Task";
}

function validateForm() {
    // Check if all required fields are filled
    const person = document.getElementById('person').value.trim();
    const title = document.getElementById('title').value.trim();
    const description = document.getElementById('description').value.trim();
    const status =  document.getElementById('status').value.trim();
    const isFormValid = person && title && description && status; // Simple truthy check

    // Enable or disable the button based on the form validity
    document.getElementById('add-update-form-button').disabled = !isFormValid;
}

document.getElementById('task-form').addEventListener('input', validateForm);

// Initial setup
window.onload = function() {
    setupFormTitle();
    setupAddButton();
    validateForm()
    loadTasksTable();
};

