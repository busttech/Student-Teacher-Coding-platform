const form = document.getElementById('addQuestionForm');
const testCasesDiv = document.getElementById('testCases');
const addTestCaseBtn = document.getElementById('addTestCase');

// Add a new test case input field when the "Add Test Case" button is clicked
addTestCaseBtn.addEventListener('click', () => {
    const testCaseDiv = document.createElement('div');
    testCaseDiv.className = 'test-case';
    testCaseDiv.innerHTML = `
        <label>Input:</label>
        <input type="text" class="test-input" required>
        <label>Expected Output:</label>
        <input type="text" class="test-output" required>
        <button type="button" class="removeTestCase">Remove</button>
    `;
    testCasesDiv.appendChild(testCaseDiv);

    // Remove the test case when the "Remove" button is clicked
    testCaseDiv.querySelector('.removeTestCase').addEventListener('click', () => {
        testCasesDiv.removeChild(testCaseDiv);
    });
});

// Handle form submission to add a new question
form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the default form submission

    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const functionName = document.getElementById('functionName').value;
    const parameters = document.getElementById('parameters').value;

    // Gather all test cases (inputs and expected outputs)
    const testCases = [];
    const inputs = document.querySelectorAll('.test-input');
    const outputs = document.querySelectorAll('.test-output');

    for (let i = 0; i < inputs.length; i++) {
        testCases.push({ input: inputs[i].value, output: outputs[i].value });
    }

    // Send the question and test case data to the server
    const response = await fetch('/teacher', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title,
            description,
            function_name: functionName,
            parameters,
            test_cases: testCases
        })
    });

    if (response.ok) {
        alert('Question added successfully!');
        form.reset();
        testCasesDiv.innerHTML = ''; // Clear all test case inputs after submission
    } else {
        alert('Failed to add the question. Please try again.');
    }
});
