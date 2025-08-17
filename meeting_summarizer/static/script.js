function generateSummary() {
    const transcript = document.getElementById('transcript').value;
    const prompt = document.getElementById('prompt').value;

    fetch('/generate_summary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `transcript=${encodeURIComponent(transcript)}&prompt=${encodeURIComponent(prompt)}`
    })
    .then(response => response.json())
    .then(data => {
        if(data.summary){
            document.getElementById('summary').value = data.summary;
        } else {
            document.getElementById('status').innerText = data.error;
        }
    });
}

function sendEmail() {
    const recipients = document.getElementById('recipients').value;
    const summary = document.getElementById('summary').value;

    fetch('/send_email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `recipients=${encodeURIComponent(recipients)}&summary=${encodeURIComponent(summary)}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').innerText = data.success || data.error;
    });
}