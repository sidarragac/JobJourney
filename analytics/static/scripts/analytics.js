function sortRoadmaps(higher){
    var roadmapsList = document.getElementById('Roadmaps');
    var roadmaps = Array.from(roadmapsList.getElementsByClassName('roadmap'));
    roadmaps.sort((a,b) => {
        var likesA = parseInt(a.getAttribute('likes'));
        var likesB = parseInt(b.getAttribute('likes'));
        if(higher){
            return likesB - likesA;
        }else{
            return likesA - likesB;
        }
    });
    roadmapsList.innerHTML = "";
    roadmaps.forEach(roadmap => roadmapsList.appendChild(roadmap));
}