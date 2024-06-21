function generateCaption() {
    const imageInput = document.getElementById('imageUpload');
    const uploadedImage = document.getElementById('uploadedImage');
    const captionText = document.getElementById('captionText');

    if (imageInput.files && imageInput.files[0]) {
        const formData = new FormData();
        formData.append('image', imageInput.files[0]);

        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.caption) {
                captionText.textContent = data.caption;
            } else if (data.error) {
                captionText.textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            captionText.textContent = 'Error generating caption.';
        });

        // Display the uploaded image
        const reader = new FileReader();
        reader.onload = function(e) {
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = 'block';
        }
        reader.readAsDataURL(imageInput.files[0]);
    } else {
        alert('Please upload an image first.');
    }
}
