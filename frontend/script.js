function generateCaption() {
    const imageInput = document.getElementById('imageUpload');
    const uploadedImage = document.getElementById('uploadedImage');
    const captionText = document.getElementById('captionText');

    if (imageInput.files && imageInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = 'block';

            // Here you would make an API call to your backend to generate the caption.
            // For the purpose of this example, we will use a static caption.
            // Example API call (uncomment and modify accordingly):
            // fetch('YOUR_API_ENDPOINT', {
            //     method: 'POST',
            //     body: JSON.stringify({ image: e.target.result }),
            //     headers: { 'Content-Type': 'application/json' }
            // })
            // .then(response => response.json())
            // .then(data => {
            //     captionText.textContent = data.caption;
            // })
            // .catch(error => {
            //     console.error('Error:', error);
            // });

            // Static caption for demonstration
            captionText.textContent = 'A sample generated caption for the uploaded image.';
        }

        reader.readAsDataURL(imageInput.files[0]);
    } else {
        alert('Please upload an image first.');
    }
}
