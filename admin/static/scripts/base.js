let subMenu = document.getElementById("subMenu");
let subMenuu = document.getElementById("subMenuu");

function toggleMenu(){
    subMenu.classList.toggle("open-menu");
    subMenuu.classList.toggle("open-menu");
}

function showTranslate(){
    let translate = document.getElementById("google_translate_element");
    if (translate.style.display === "block") {
        translate.style.display = "none";
    } else {
        translate.style.display = "block";
    }
}