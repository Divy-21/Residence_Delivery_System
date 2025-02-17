document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const searchTerm = document.getElementById('searchTerm').value;

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `searchTerm=${encodeURIComponent(searchTerm)}`,
    })
    .then(response => response.json())
    .then(data => {
        const resultsContainer = document.getElementById('results');
        resultsContainer.innerHTML = '';
        if (data.length > 0) {
            data.forEach(item => {
                const div = document.createElement('div');
                div.textContent = item.name;
                resultsContainer.appendChild(div);
            });
        } else {
            resultsContainer.textContent = 'No results found';
        }

        // Change the input field to text and update the search button
        const searchInput = document.getElementById('searchTerm');
        searchInput.outerHTML = `<span id="searchTerm">${searchTerm}</span>`;
        document.getElementById('searchButton').style.display = 'none';
        document.getElementById('resetButton').style.display = 'inline';
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('resetButton').addEventListener('click', function() {
    // Change the text back to an input field and reset the form
    const searchTermSpan = document.getElementById('searchTerm');
    searchTermSpan.outerHTML = `<input type="text" id="searchTerm" name="searchTerm" placeholder="Search...">`;
    document.getElementById('searchButton').style.display = 'inline';
    document.getElementById('resetButton').style.display = 'none';
    document.getElementById('results').innerHTML = '';
});

