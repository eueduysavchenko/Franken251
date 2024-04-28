function createButton(text, onClickFunction) {
    const button = document.createElement('button');
    button.type = 'button';
    button.innerText = text;
    button.onclick = onClickFunction;
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
    const id = document.getElementById('id').value;  // Отримуємо ID, якщо воно вказано
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
    // setupAddButton(); // Reset button to 'Add'
}

function updateTask(id, data) {
    console.log('Updating task:', id, data);
    resetAddUpdateForm();
    setupFormTitle();
    setupAddButton(); // Reset button to 'Add'
}

function loadUpdateForm(id) {
    console.log('Loading task data to update:', id);
    fetch(`/api/tasks/${id}`, {
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
            document.getElementById('id').value = task.id;
            document.getElementById('person').value = task.person;
            document.getElementById('title').value = task.title;
            document.getElementById('description').value = task.description;
            document.getElementById('status').value = task.status;
        })
        .catch(error => console.error('Error:', error));
    setupFormTitle(false);
    setupUpdateButton(); // Change button to 'Update'
}

function deleteTask(id) {
    fetch(`/api/tasks/${id}`, {
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
    document.getElementById('id').value = '';
}

function setupFormTitle(isAddTask = true) {
    document.getElementById('form-title').innerText = isAddTask ? "Add Task" : "Update Task";
}

// Initial setup
window.onload = function() {
    setupFormTitle();
    setupAddButton();
    loadTasksTable();
};

