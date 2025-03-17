let videoElement = document.getElementById('preview');
let resultDiv = document.getElementById('scan-result');

// Request camera access
navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
.then(stream => {
    videoElement.srcObject = stream;
    videoElement.play();
    requestAnimationFrame(tick);
})
.catch(err => {
    resultDiv.innerHTML = "❌ Error accessing camera: " + err;
});

function tick() {
    if (videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);
        
        if (code) {
            verifyCode(code.data);
        }
    }
    requestAnimationFrame(tick);
}

async function verifyCode(qrData) {
    try {
        const response = await fetch('/verify_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `qr_data=${encodeURIComponent(qrData)}`
        });
        
        const result = await response.text();
        resultDiv.innerHTML = result;
        
        // Add sound feedback
        if (result.includes("✅")) {
            new Audio('/static/success.mp3').play();
        } else {
            new Audio('/static/error.mp3').play();
        }
        
    } catch (error) {
        resultDiv.innerHTML = "❌ Verification failed: Server error";
        console.error('Verification error:', error);
    }
}