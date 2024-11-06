function toggleFields() {
    var radioButton = document.getElementById('btnradio2').checked;
    var isCompany = document.getElementById('isCompany');

    var companyFields = document.getElementById('companyFields');
    var personFields = document.getElementById('personFields');
    var companyName = document.getElementById('companyName');
    var first_name = document.getElementById('first_name');
    var last_name = document.getElementById('last_name');


    if (radioButton) {
        companyFields.style.display = 'block';
        personFields.style.display = 'none';
        companyName.required = true;
        first_name.required = false;
        last_name.required = false;
        isCompany.value = true;
    } else {
        companyFields.style.display = 'none';
        personFields.style.display = 'block';
        companyName.required = false;
        first_name.required = true;
        last_name.required = true;
        isCompany.value = false;
    }
}

window.onload = function() {
    document.getElementById('btnradio2').checked = document.getElementById('isCompany').value === 'true';
    toggleFields();  // Set the correct fields visibility on page load
};

document.getElementById('password2').addEventListener('keyup', () => {
    var password1 = document.getElementById('password1');
    var password2 = document.getElementById('password2');
    if (password1.value === password2.value && password1.value !== "") {
        password2.style.borderBottom = "2px solid green";
    } else {
        password2.style.borderBottom = "2px solid red";
    }
});

document.getElementById('password1').addEventListener('keyup', () => {
    var password1 = document.getElementById('password1');
    var password2 = document.getElementById('password2');
    if (password1.value === password2.value && password1.value !== "") {
        password2.style.borderBottom = "2px solid green";
    } else {
        password2.style.borderBottom = "2px solid red";
    }
});

document.getElementById('dateOfBirth').addEventListener('change', () => {
    let dateOfBirth = document.getElementById('dateOfBirth');
    let age = new Date().getFullYear() - new Date(dateOfBirth.value).getFullYear();
    let button = document.getElementById('submitButton');
    if(age <= 0){
        button.disabled = true;
        dateOfBirth.style.borderBottom = "2px solid red";
    }else{
        button.disabled = false;
        dateOfBirth.style.borderBottom = "1px solid black";
    }
});
