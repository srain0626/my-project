let lastInputText = '';

document.addEventListener('input', function(event) {
  if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
    const inputText = event.target.value;
    const lastChar = inputText.slice(-1);

    if (lastChar === '.' || lastChar === '!' || lastChar === '?') {
      fetch('http://127.0.0.1:5000/correct', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText })
      })
      .then(response => response.json())
      .then(data => {
        event.target.value = data.corrected_text;
        lastInputText = data.corrected_text;
      })
      .catch(error => console.error('Error:', error));
    } else {
      lastInputText = inputText;
    }
  }
});
