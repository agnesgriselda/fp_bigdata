document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultDiv = document.getElementById('result');
    const predictionOutput = document.getElementById('prediction-output');
    const submitBtn = document.getElementById('submit-btn');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const originalButtonText = submitBtn.textContent;
        submitBtn.textContent = 'Memprediksi...';
        submitBtn.disabled = true;

        const formData = new FormData(form);
        const data = {
            age: parseInt(formData.get('age')),
            sex: formData.get('sex'),
            bmi: parseFloat(formData.get('bmi')),
            children: parseInt(formData.get('children')),
            smoker: formData.get('smoker'),
            region: formData.get('region')
        };

        try {
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await response.json();

            if (result.error) {
                throw new Error(result.error);
            }
            
            const formattedResult = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(result.predicted_charges);
            predictionOutput.textContent = formattedResult;
            resultDiv.style.display = 'block';

        } catch (error) {
            predictionOutput.textContent = `Error: ${error.message}`;
            resultDiv.style.display = 'block';
        } finally {
            submitBtn.textContent = originalButtonText;
            submitBtn.disabled = false;
        }
    });
});