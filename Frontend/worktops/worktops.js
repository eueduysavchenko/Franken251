function createButton(text, onClickFunction) {
    const button = document.createElement('button');
    button.type = 'button';
    button.innerText = text;
    button.onclick = onClickFunction;
    return button;
}

function setupAddButton() {
    document.getElementById('add-button').style.display = 'inline-block';
    document.getElementById('update-button').style.display = 'none';
    document.getElementById('delete-button').style.display = 'none';
}

function setupUpdateDeleteButtons() {
    document.getElementById('add-button').style.display = 'none';
    document.getElementById('update-button').style.display = 'inline-block';
    document.getElementById('delete-button').style.display = 'inline-block';
}

function submitForm(action) {
    const id = document.getElementById('quest-id').value;
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

    if (action === 'add') {
        addQuest(data);
    } else if (action === 'update') {
        updateQuest(id, data);
    } else if (action === 'delete') {
        deleteQuest(id);
    }
}

function addQuest(data) {
    console.log('Adding quest:', data);
    fetch('/api/quests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        resetAddUpdateForm();
        loadQuestsTable();
    })
    .catch(error => console.error('Error:', error));
}

function updateQuest(quest_id, data) {
    console.log('Updating quest:', quest_id, data);
    fetch(`/api/quests/${quest_id}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(() => {
        resetAddUpdateForm();
        loadQuestsTable();
    })
    .catch(error => console.error('Error:', error));
}

function deleteQuest(quest_id) {
    console.log('Deleting quest:', quest_id);
    fetch(`/api/quests/${quest_id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            loadQuestsTable();
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function loadUpdateForm(quest_id) {
    console.log('Loading quest data to update:', quest_id);
    fetch(`/api/quests/${quest_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Quest not found');
        }
        return response.json();
    })
    .then(quest => {
        document.getElementById('quest-id').value = quest.id;
        document.getElementById('person').value = quest.person;
        document.getElementById('title').value = quest.title;
        document.getElementById('description').value = quest.description;
        document.getElementById('status').value = quest.status;

        setupFormTitle(false);
        setupUpdateDeleteButtons();
    })
    .catch(error => console.error('Error:', error));
}

function loadQuestsTable() {
    fetch('/api/quests')
    .then(response => response.json())
    .then(quests => {
        const questsList = document.getElementById('quests-list');
        questsList.innerHTML = '';
        quests.forEach(quest => {
            const row = questsList.insertRow();
            row.innerHTML = `
                <td>${quest.id}</td>
                <td>${quest.person}</td>
                <td>${quest.title}</td>
                <td>${quest.description}</td>
                <td>${quest.status}</td>
                <td class="table-button-cell">
                    <button class="table-button update-quest-button" onclick="loadUpdateForm(${quest.id})">✍️</button>
                    <button class="table-button delete-quest-button" onclick="deleteQuest(${quest.id})">❌</button>
                </td>
            `;
        });
    });
}

function resetAddUpdateForm() {
    setupFormTitle();
    setupAddButton();
    document.getElementById('quest-form').reset();
    document.getElementById('quest-id').value = '';
}

function setupFormTitle(isAddQuest = true) {
    document.getElementById('form-title').innerText = isAddQuest ? "Add Quest" : "Update Quest";
}

document.getElementById('quest-form').addEventListener('input', validateForm);

window.onload = function() {
    setupFormTitle();
    setupAddButton();
    loadQuestsTable();
};
