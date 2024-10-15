const placeholders = {
    1: "Ex: Researcher in Biology",
    2: "Ex: Data Analyst at a financial firm",
    3: "Ex: Software engineer at Google",
    4: "Ex: Doctor specializing in Pediatrics",
    5: "Ex: Sociologist working in public policy",
    6: "Ex: Historian or Professor of Literature",
    7: "Ex: Graphic Designer at a creative agency",
    8: "Ex: Marketing Manager in a tech company",
    9: "Ex: Corporate Lawyer in a law firm",
    10: "Ex: Elementary School Teacher",
    11: "Ex: Cybersecurity Specialist",
    12: "Ex: Environmental Consultant",
    13: "Ex: Journalist at a major news outlet",
    14: "Ex: Urban Planner with a focus on sustainability",
};

window.onload = function(){
    var slider = document.getElementById("salary");
    var value = document.getElementById("value");
    value.innerHTML = slider.value;
}

document.getElementById('interest').addEventListener('change', function() {
    const selectedArea = this.value;
    const objectiveInput = document.getElementById('objective');
    
    if (placeholders[selectedArea]) {
        objectiveInput.placeholder = placeholders[selectedArea];
    } else {
        objectiveInput.placeholder = "Ex: Software engineer at Google";
    }
});

function changeValue(slidervalue) {
    var value = document.getElementById('value');
    value.innerHTML = slidervalue.value;
}

document.getElementById('interestForm').onsubmit = function() {
    // Show the loading screen
    document.getElementById('loading-screen').style.display = 'block';
    document.getElementById('content-container').classList.add('blurry');
    return true;
};