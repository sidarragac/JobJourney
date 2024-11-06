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

function setReadOnly(){
    let fields = ['email', 'password1', 'password2', 'first_name', 'last_name'];
    fields.forEach(field => {
        document.getElementById(field).style.pointerEvents = 'none';
    });
}

window.onload = function() {
    document.getElementById('btnradio2').checked = document.getElementById('isCompany').value === 'true';
    toggleFields();  // Set the correct fields visibility on page load
    setReadOnly(); // Set the already filled fields to be read only
};