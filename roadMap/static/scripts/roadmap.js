window.onload = function(){
    initializeCheckboxes();
    locateStep();
    loadProgress();
    showInfo();
}

function initializeCheckboxes(){
    let numChkpts = 1; // Initialize counter
    const checkpoints = JSON.parse(document.getElementById('checkpoints-data').textContent);
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="remarkablePoint"]');
    checkboxes.forEach(checkbox => {
        checkbox.value = numChkpts;
        if(checkpoints[numChkpts]){
            checkbox.checked = true;    
        }else{
            checkbox.checked = false;
        }
        numChkpts++;
    });
}


function locateStep(){
    const url = window.location.pathname;
    const splittedUrl = url.split('/');
    const stepNumber = parseInt(splittedUrl[splittedUrl.length-1]);
    if(splittedUrl.length == 5 && stepNumber > 0){ //Must be equal to 5 to be an after mark page.
        openModal(stepNumber);
    }
}

function openModal(step){
    //Open the modal of the step element with the given id.
    const stepElement = document.getElementById('modal'+step);
    if(stepElement){
        stepElement.showModal();
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

function loadProgress(){
    let count = 0
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="remarkablePoint"]');
    for(count = 0; count < checkboxes.length; count++){
        if(!checkboxes[count].checked){
            break
        }
    }
    console.log(count);
        if(count >= 15){
            document.getElementById('paso1').classList.add('active');
            document.getElementById('paso2').classList.add('active');
            document.getElementById('paso3').classList.add('active');
            document.getElementById('paso4').classList.add('active');
            document.getElementById('paso5').classList.add('active');
    }else if(count >= 12){
        document.getElementById('paso1').classList.add('active');
        document.getElementById('paso2').classList.add('active');
        document.getElementById('paso3').classList.add('active');
        document.getElementById('paso4').classList.add('active');
        document.getElementById('paso5').classList.remove('active');
    }else if(count >= 9){
        document.getElementById('paso1').classList.add('active');
        document.getElementById('paso2').classList.add('active');
        document.getElementById('paso3').classList.add('active');
        document.getElementById('paso4').classList.remove('active');
        document.getElementById('paso5').classList.remove('active');
    }else if(count >= 6){
        document.getElementById('paso1').classList.add('active');
        document.getElementById('paso2').classList.add('active');
        document.getElementById('paso3').classList.remove('active');
        document.getElementById('paso4').classList.remove('active');
        document.getElementById('paso5').classList.remove('active');
    }else if(count >= 3){
        document.getElementById('paso1').classList.add('active');
        document.getElementById('paso2').classList.remove('active');
        document.getElementById('paso3').classList.remove('active');
        document.getElementById('paso4').classList.remove('active');
        document.getElementById('paso5').classList.remove('active');
    }
}

function showInfo(){
    const btn1 = document.getElementById('btn1');
    const btn2 = document.getElementById('btn2');
    const btn3 = document.getElementById('btn3');
    const btn4 = document.getElementById('btn4');
    const btn5 = document.getElementById('btn5');

    const close1 = document.getElementsByClassName('btn-cerrar-modal1');
    const close2 = document.getElementsByClassName('btn-cerrar-modal2');
    const close3 = document.getElementsByClassName('btn-cerrar-modal3');
    const close4 = document.getElementsByClassName('btn-cerrar-modal4');
    const close5 = document.getElementsByClassName('btn-cerrar-modal5');

    const modal1 = document.getElementById('modal1');
    const modal2 = document.getElementById('modal2');
    const modal3 = document.getElementById('modal3');
    const modal4 = document.getElementById('modal4');
    const modal5 = document.getElementById('modal5');

    btn1.addEventListener('click',() => {
        modal1.showModal();
    })

    btn2.addEventListener('click',() => {
        modal2.showModal();
    })

    btn3.addEventListener('click',() => {
        modal3.showModal();
    })

    btn4.addEventListener('click',() => {
        modal4.showModal();
    })

    btn5.addEventListener('click',() => {
        modal5.showModal();
    })

    close1[0].addEventListener('click',() => {
        modal1.close();
    })
    close1[1].addEventListener('click',() => {
        modal1.close();
    })

    close2[0].addEventListener('click',() => {
        modal2.close();
    })
    close2[1].addEventListener('click',() => {
        modal2.close();
    })

    close3[0].addEventListener('click',() => {
        modal3.close();
    })
    close3[1].addEventListener('click',() => {
        modal3.close();
    })

    close4[0].addEventListener('click',() => {
        modal4.close();
    })
    close4[1].addEventListener('click',() => {
        modal4.close();
    })

    close5[0].addEventListener('click',() => {
        modal5.close();
    })
    close5[1].addEventListener('click',() => {
        modal5.close();
    })

}