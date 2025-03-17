async function registerParticipant() {
    try {
        const formData = new FormData(document.getElementById('registrationForm'));
        const response = await fetch('/register', {
            method: 'POST',
            body: formData
        });
        
        if(response.status === 200) {
            window.location.href = '/participants';
        } else {
            const error = await response.text();
            alert(`Error: ${error}`);
        }
    } catch (error) {
        alert(`Network error: ${error}`);
    }
}

async function verifyQR() {
    try {
        const qrData = document.querySelector('[name="qr_data"]').value;
        const response = await fetch('/verify_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `qr_data=${encodeURIComponent(qrData)}`
        });
        
        if(response.ok) {
            window.location.reload();
        }
    } catch (error) {
        alert(`Verification error: ${error}`);
    }
}