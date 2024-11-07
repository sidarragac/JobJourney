window.onload = function() {
    modalSettings();
}

function modalSettings() {
    const settingButton = document.getElementById("settingsButton");
    const modal = document.getElementById("modal");
    const closeButton = document.getElementById("closeButton");

    settingButton.addEventListener("click",() => {
        modal.showModal();
    });
    closeButton.addEventListener("click",() => {
        modal.close();
    });
}

function savePicture() {
    let profilePic = document.getElementById("profilePic");
    let inputFile = document.getElementById("inputFile");
    
    inputFile.onchange = function() {
        profilePic.src = URL.createObjectURL(inputFile.files[0]);
    }
}


window.onclick = function(event) {
    if (event.target == modal) {
        modal.close();
    }
}

