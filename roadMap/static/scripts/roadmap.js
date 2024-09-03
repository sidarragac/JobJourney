window.onload = function(){
    const url = window.location.pathname;
    const splittedUrl = url.split('/');
    const stepNumber = parseInt(splittedUrl[splittedUrl.length-1]);
    if(splittedUrl.length == 4 && stepNumber > 0){
        scrollToStep("Paso"+stepNumber);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    let numChkpts = 1; // Initialize counter
    const checkpoints = JSON.parse(document.getElementById('checkpoints-data').textContent);
    console.log(checkpoints);
    
    // Function to assign values to checkboxes and increment the counter
    function initializeCheckboxes() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"][name="checkpoint"]');
        checkboxes.forEach(checkbox => {
            checkbox.value = numChkpts;
            console.log(checkbox.value);
            console.log(numChkpts);
            console.log(checkpoints[numChkpts]);
            if(checkpoints[numChkpts]){
                checkbox.checked = true;    
            }else{
                checkbox.checked = false;
            }
            numChkpts++;
        });
    }

    // Initialize checkboxes on page load
    initializeCheckboxes();
});

function scrollToStep(step){
    //Scroll to the step element with the given id.
    const stepElement = document.getElementById(step);
    if(stepElement){
        stepElement.scrollIntoView({behavior: "smooth", block: "start"});
    }
}