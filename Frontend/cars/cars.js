document.addEventListener("DOMContentLoaded", function () {
  // Функція для завантаження та відображення списку авто
  function loadCars() {
    fetch("/api/cars")
      .then((response) => response.json())
      .then((cars) => {
        const carsList = document.getElementById("cars-list");
        // Очищаємо список перед додаванням нових даних
        carsList.innerHTML = "";
        cars.forEach((cars) => {
          const row = carsList.insertRow();
          row.innerHTML = `
                        <td>${cars.id}</td>
                        <td>${cars.factory}</td>
                        <td>${cars.models_name}</td>
                        <td>${cars.country_name}</td>
                        <td>${cars.engine_size}</td>
                    `;
        });
      });
  }

  // Викликаємо функцію для ініціалізації списку студентів
  loadCars();

  // EventHandler для форми додавання нового авто
  document
    .getElementById("cars-form")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      const id = document.getElementById("id").value; // Отримуємо ID, якщо воно вказано
      const factory = document.getElementById("factory").value;
      const models_name = document.getElementById("models_name").value;
      const country_name = document.getElementById("country_name").value;
      const engine_size = document.getElementById("engine_size").value;

      const data = {
        id: id,
        group: factory,
        first_name: models_name,
        last_name: country_name,
        score: engine_size,
      };

      // Відправляємо дані на сервер для додавання або оновлення студента
      fetch("/api/cars", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then(() => {
          // Очищаємо форму після додавання авто
          document.getElementById("cars-form").reset();
          // Видаляємо значення ID для уникнення непередбачуваної поведінки
          document.getElementById("id").value = "";
          // Оновлюємо список авто на сторінці
          loadStudents();
        })
        .catch((error) => console.error("Error:", error));
    });
});
