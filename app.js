document.getElementById('summarize-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const url_or_text = document.getElementById('url_or_text').value;

    console.log('Sending request...');
    try {
        const response = await fetch('http://localhost:5000/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url_or_text: url_or_text })
        });
        console.log('Response:', response);

        const result = await response.json();
        document.getElementById('summary').innerText = result.summary;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('summary').innerText = 'Failed to summarize the article. Please try again.';
    }
});
