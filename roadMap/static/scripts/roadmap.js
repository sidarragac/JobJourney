function submit(checkbox, step){
    checkbox.value = checkbox.value * step;

    checkbox.form.submit();
}