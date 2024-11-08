function updateOptions(){
    const selectedValues = Array.from(document.querySelectorAll('.interestOption'))
        .map(select => select.value)
        .filter(value => value);
    
    document.querySelectorAll('.interestOption').forEach(select => {
        Array.from(select.options).forEach(option => {
            option.hidden = false;
        });

        selectedValues.forEach(value => {
            if (select.value !== value) {
                const option = select.querySelector(`option[value="${value}"]`);
                if (option) option.hidden = true;
            }
        });
    });
}

window.onload = function() {
    updateOptions();
}