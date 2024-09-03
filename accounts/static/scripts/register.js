function toggleFields() {
    var radioButton = document.getElementById('btnradio2').checked;
    var content = "";
    var dataFields = document.getElementById('content');

    var isCompany = document.getElementById('isCompany');

    if (radioButton) {
        isCompany.value = "True";
        content = `
            <div class="input-box">
                <div class="input-field">
                    <input type="text" class="input" id="city" name="city" required autocomplete="off">
                    <label for="city">City</label>
                </div>
                <div id="companyFields">
                    <!-- Company fields -->
                    <div class="input-field">
                        <input type="text" class="input" id="companyName" name="companyName" autocomplete="off">
                        <label for="companyName">Company Name</label>
                    </div>
                </div>
            </div>
        `;
    } else {
        isCompany.value = "False";
        content = `
            <div class="input-box">
                <div class="input-field">
                    <input type="text" class="input" id="city" name="city" required autocomplete="off">
                    <label for="city">City</label>
                </div>
                <!-- Person fields -->
                <div id="personFields">
                    <div class="input-field">
                        <input type="text" class="input" id="first_name" name="first_name" required autocomplete="off">
                        <label for="first_name">First Name</label>
                    </div>
                    <div class="input-field">
                        <input type="text" class="input" id="last_name" name="last_name" required autocomplete="off">
                        <label for="last_name">Last Name</label>
                    </div>
                    <!-- birth date -->
                    <div class="input-field">
                        <input type="date" class="input" id="dateOfBirth" name="dateOfBirth" placeholder="">
                        <label for="dateOfBirth">Birth Date</label>
                    </div>
                </div>
            </div>
        `;
    }
    dataFields.innerHTML = content;
}

window.onload = function() {
    toggleFields();  // Set the correct fields visibility on page load
};