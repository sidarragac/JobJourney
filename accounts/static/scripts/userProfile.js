const settingButton = document.getElementById("settingsButton");
const modal = document.getElementById("modal");

settingButton.addEventListener("click",() => {
    modal.showModal();
});

let profilePic = document.getElementById("profilePic");
let inputFile = document.getElementById("inputFile");

inputFile.onchange = function() {
    profilePic.src = URL.createObjectURL(inputFile.files[0]);
}
