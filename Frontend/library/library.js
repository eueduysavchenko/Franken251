document.addEventListener('DOMContentLoaded', function() {
    // Функція для завантаження та відображення списку книжок
    function loadBooks() {
        fetch('/api/library')
            .then(response => response.json())
            .then(books => {
                const booksList = document.getElementById('books-list');
                // Очищаємо список перед додаванням нових даних
                booksList.innerHTML = '';
                books.forEach(book => {
                    const row = booksList.insertRow();
                    row.innerHTML = `
                        <td>${book.id}</td>
                        <td>${book.author}</td>
                        <td>${book.title}</td>
                        <td>${book.taken}</td>
                    `;
                });
            });
    }

    // Викликаємо функцію для ініціалізації списку книжок
    loadBooks();

    // EventHandler для форми додавання нової книжки
    document.getElementById('book-form').addEventListener('submit', function(event) {
        event.preventDefault();

        console.log('book-form-submit called')

        const author = document.getElementById('author').value;
        const title = document.getElementById('title').value;

        const data = {
            author: author,
            title: title
        };

        // Відправляємо дані на сервер для додавання книжки
        fetch('/api/library', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(() => {
            // Очищаємо форму після додавання книжки
            document.getElementById('book-form').reset();
            // Оновлюємо список книжок на сторінці
            loadBooks();
        })
        .catch(error => console.error('Error:', error));
    });
});
