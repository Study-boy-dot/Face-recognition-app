document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    const imageFile = document.getElementById('image').files[0];
    formData.append('image', imageFile);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        // if (imageFile.size > 100 * 1024) { // Check if file size is greater than 100KB
        //     alert("File size exceeds 100KB.");
        //     return;
        // }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            console.log("Backend response:", data);
            const timestamp = new Date().getTime();
            const outputImagePath = `${data.output_image}?t=${timestamp}`;
            document.getElementById('outputImage').src = outputImagePath;
            document.getElementById('outputImage').style.display = 'block';
            document.getElementById('responseText').innerText = 'Successfully Inference';
            console.log("Successfully Inference");
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while processing the image: ' + error.message);
    }
});
