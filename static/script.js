function correctText() {
    const inputText = document.getElementById('inputText').value;
    fetch('/correct', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText })
    })
    .then(response => response.json())
    .then(data => {
        const correctionsDiv = document.getElementById('corrections');
        correctionsDiv.innerHTML = '';
        data.corrections.forEach(correction => {
            const p = document.createElement('p');
            p.innerText = `Error: ${correction.message}, Suggestion: ${correction.replacement}`;
            correctionsDiv.appendChild(p);
        });
    });
}
