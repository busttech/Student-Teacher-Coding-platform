const runCodeBtn = document.getElementById('runCode');
const submitCodeBtn = document.getElementById('submitCode');
const resultDiv = document.getElementById('result');
const codeArea = document.getElementById('code');
const form = document.getElementById('codeForm');
const warningMessage = document.getElementById('warningMessage');
const code1 = codeArea.value;
const screenWidth1 = window.innerWidth;
const screenHeight1 = window.innerHeight;
let warningCount = 0;
let warningCoun = 0;
runCodeBtn.addEventListener('click', async (event) => {
    event.preventDefault();
    const code = codeArea.value;
    if (code.trim() === "") {
        warningCoun++;
        warningMessage.textContent = `Warning ${warningCoun}: You haven't written any code.`;
        warningMessage.style.display = 'block';
        if (warningCoun >= 5) {
            alert('You have received 5 warnings. The page will now refresh.');
            window.location.reload();
        }
        return;
    }
    warningMessage.style.display = 'none';
    resultDiv.textContent = 'Running...';
    resultDiv.classList.remove('error');
    try {
        const response = await fetch('/run_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });
        const data = await response.json();
        resultDiv.textContent = data.output || 'No output.';
    } catch (err) {
        resultDiv.textContent = 'Error running code.';
    }
});
submitCodeBtn.addEventListener('click', async (event) => {
    event.preventDefault();
    const code = codeArea.value;
    if (code.trim() === "") {
        alert('Please write some code before submitting.');
        return;
    }
    warningMessage.style.display = 'none';
    resultDiv.textContent = 'Submiting...';
    resultDiv.classList.remove('error');
    const questionId = window.location.pathname.split('/').pop();
    try {
        const response = await fetch(`/submit_code/${questionId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });
        const data = await response.json();
        if (data.status === 'success') {
            resultDiv.textContent = 'Code passed all test cases!';
            resultDiv.classList.add('success');
            resultDiv.classList.remove('error');
        } else {
            resultDiv.textContent = 'Code failed some test cases.';
            resultDiv.classList.add('error');
            resultDiv.classList.remove('success');
            let failedResultsHtml = '<ul>';
            let pas = 0;
            for (let result of data.results) {
                const { input, expected, output, passed } = result;
                if(passed){
                    pas++;
                }
                if (!passed) {
                    pas++
                    failedResultsHtml += `
                        <li style="color: red;">
                            <strong>Test Case Number:</strong>${pas} <br>
                            <strong>Input:</strong> ${input} <br>
                            <strong>Expected Output:</strong> ${expected} <br>
                            <strong>Output:</strong> ${output} <br>
                            <strong>Status:</strong> Failed
                        </li>
                    `;
                    break;
                }
            }
            failedResultsHtml += '</ul>';
            resultDiv.innerHTML = failedResultsHtml;
        }
    } catch (err) {
        resultDiv.textContent = 'Error submitting code.';
        resultDiv.classList.add('error');
    }
});
codeArea.addEventListener('keydown', function(event) {
    const cursorPosition = codeArea.selectionStart;
    const codeText = codeArea.value;
    const pairs = {
        '(': ')',
        '{': '}',
        '[': ']',
        '"': '"',
        "'": "'"
    };
    if (pairs[event.key]) {
        const openChar = event.key;
        const closeChar = pairs[openChar];
        codeArea.value = 
            codeText.substring(0, cursorPosition) + 
            openChar + closeChar + 
            codeText.substring(cursorPosition);
        codeArea.setSelectionRange(cursorPosition + 1, cursorPosition + 1);
        event.preventDefault();
    }
    if (event.key === 'Enter') {
        const lines = codeText.substring(0, cursorPosition).split('\n');
        const lastLine = lines[lines.length - 1];
        const currentIndentation = lastLine.match(/^\s*/)[0];
        const additionalIndentation = lastLine.trim().endsWith(':') ? '    ' : '';
        codeArea.value = 
            codeText.substring(0, cursorPosition) + '\n' + 
            currentIndentation + additionalIndentation + 
            codeText.substring(cursorPosition);
        codeArea.setSelectionRange(
            cursorPosition + currentIndentation.length + additionalIndentation.length + 1, 
            cursorPosition + currentIndentation.length + additionalIndentation.length + 1
        );
        event.preventDefault();
    }
});
function handleScreenResize() {
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;
    if (screenWidth < screenWidth1 || screenHeight < screenHeight1) {
        codeArea.disabled = true;
        codeArea.value = "";
        warningMessage.textContent = "Code editor is disabled because the screen is too small or split.";
        warningMessage.style.display = 'block';
    } else {
        codeArea.disabled = false;
        codeArea.value = code1;
        warningMessage.style.display = 'none';
    }
}
window.addEventListener('resize', handleScreenResize);
handleScreenResize();
codeArea.addEventListener('copy', function(event) {
    event.preventDefault();
    alert('Copying is disabled in this editor.');
});
codeArea.addEventListener('cut', function(event) {
    event.preventDefault();
    alert('Cutting is disabled in this editor.');
});
codeArea.addEventListener('paste', function(event) {
    event.preventDefault();
    alert('Pasting is disabled in this editor.');
});
codeArea.addEventListener('dragstart', function(event) {
    event.preventDefault();
});
codeArea.addEventListener('dragover', function(event) {
    event.preventDefault();
});
codeArea.addEventListener('drop', function(event) {
    event.preventDefault();
    alert('Drag and drop is disabled in this editor.');
});
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        warningCount++;
        warningMessage.textContent = `Warning ${warningCount}: You've switched tabs.`;
        warningMessage.style.display = 'block';
        if (warningCount >= 2) {
            alert('You have received 2 warnings. The page will now refresh.');
            codeArea.value = "";
            codeArea.value = code1;
            window.location.reload();
        }
    }
});
