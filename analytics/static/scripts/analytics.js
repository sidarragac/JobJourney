const chartOne = document.getElementById("chartOne");
const chartTwo = document.getElementById("chartTwo");

chartOne.addEventListener("mouseover", () => {
    chartOne.style.width = "600px";
    chartTwo.style.width = "200px";
});
chartOne.addEventListener("mouseout", () => {
    chartOne.style.width = "500px";
    chartTwo.style.width = "400px";
});

chartTwo.addEventListener("mouseover", () => {
    chartTwo.style.width = "500px";
    chartOne.style.width = "350px";
});

chartTwo.addEventListener("mouseout", () => {
    chartTwo.style.width = "400px";
    chartOne.style.width = "500px";
});