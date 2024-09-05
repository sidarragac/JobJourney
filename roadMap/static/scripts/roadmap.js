window.onload = function(){
    const url = window.location.pathname;
    const splittedUrl = url.split('/');
    const stepNumber = parseInt(splittedUrl[splittedUrl.length-1]);
    if(splittedUrl.length == 4 && stepNumber > 0){
        scrollToStep("Paso"+stepNumber);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    let numChkpts = 1; // Initialize counter
    const checkpoints = JSON.parse(document.getElementById('checkpoints-data').textContent);
    
    // Function to assign values to checkboxes and increment the counter
    function initializeCheckboxes() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"][name="remarkablePoint"]');
        console.log(checkboxes);
        checkboxes.forEach(checkbox => {
            checkbox.value = numChkpts;
            console.log(numChkpts);
            console.log(checkbox.value);
            if(checkpoints[numChkpts]){
                checkbox.checked = true;    
            }else{
                checkbox.checked = false;
            }
            numChkpts++;
        });
    }

    initializeCheckboxes();
});

function scrollToStep(step){
    //Scroll to the step element with the given id.
    const stepElement = document.getElementById(step);
    if(stepElement){
        stepElement.scrollIntoView({behavior: "smooth", block: "start"});
    }
}

function submitForm(checkbox, step){
    let checkpoint = document.getElementById('checkpoint'+step);
    checkpoint.value = checkbox.value;
    //Rename the id and name to have a single POST value.
    checkpoint.id = 'checkpoint'; 
    checkpoint.name = 'checkpoint';

    checkbox.form.submit();
}