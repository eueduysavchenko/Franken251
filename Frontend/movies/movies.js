document.addEventListener('DOMContentLoaded', function() {
    function deleteMovie(movieId){
        fetch(`/api/movies/${movieId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(() => {
            loadMovies();
        })
        .catch(error => console.error('Error:', error));
    }

    function updateMovie(data){
        const loader = document.getElementById('loader');

        fetch(`/api/movies`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(() => {
            loadMovies();

            const updateButton = document.querySelector(`.update-${data.id}`);
            updateButton.style.backgroundColor = 'lightgreen';
            setTimeout(() => {
                updateButton.style.backgroundColor = '';
            }, 1500);

        })
        .catch(error => console.error('Error:', error));
    }

    function loadMovies() {
        fetch('/api/movies')
            .then(response => response.json())
            .then(movies => {
                const moviesList = document.getElementById('movies-list');
                moviesList.innerHTML = '';
                movies.forEach(movie => {
                    const row = moviesList.insertRow();

                console.log(row);
                    row.innerHTML = `
                        <td>${movie.id}</td>
                        <td><input class="title" value='${movie.title}'></td>
                        <td><input class="director" value='${movie.director}'></td>
                        <td><input class="genre" value='${movie.genre}'></td>
                        <td><input class="year_released" value=${movie.year_released}></td>
                        <td><input class="rating" value=${movie.rating}></td>
                        <td>
                            <input class="delete-${movie.id}" type="button" value="Delete" data-movie-id="${movie.id}">
                            <input class="update-${movie.id}" type="button" value="Update" data-movie-id="${movie.id}">                            
                        </td>
                    `;
                    const deleteButton = row.querySelector(`.delete-${movie.id}`);
                    deleteButton.addEventListener('click', function() {
                        const movieId = this.getAttribute('data-movie-id');
                        deleteMovie(movieId);
                    });

                    const updateButton = row.querySelector(`.update-${movie.id}`);
                    updateButton.addEventListener('click', function(event) {
                        const id = this.getAttribute('data-movie-id');
                        const title = event.target.parentNode.parentNode.querySelector('.title').value;
                        const director = event.target.parentNode.parentNode.querySelector('.director').value;
                        const genre = event.target.parentNode.parentNode.querySelector('.genre').value;
                        const year_released = event.target.parentNode.parentNode.querySelector('.year_released').value;
                        const rating = event.target.parentNode.parentNode.querySelector('.rating').value;

                        const updatedMovie = {
                            id: id,
                            title: title,
                            director: director,
                            genre: genre,
                            year_released: year_released,
                            rating: rating
                        };

                        updateMovie(updatedMovie);
                    });
                });
            });
    }

    loadMovies();

    document.getElementById('movie-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const id = document.getElementById('id').value;
        const title = document.getElementById('title').value;
        const director = document.getElementById('director').value;
        const genre = document.getElementById('genre').value;
        const year_released = document.getElementById('year_released').value;
        const rating = document.getElementById('rating').value;

        const data = {
            id: id,
            title: title,
            director: director,
            genre: genre,
            year_released: year_released,
            rating: rating
        };

        fetch('/api/movies', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(() => {
            document.getElementById('movie-form').reset();
            document.getElementById('id').value = '';
            loadMovies();
        })
        .catch(error => console.error('Error:', error));
    });
});
