function verifyRequired(){
    var interest = document.getElementById('interest');
    var objective = document.getElementById('objective');
    
    if(interest.value != ""){
        objective.required = false;
    }else if(objective.value != ""){
        interest.required = false;
    }else if(interest.value == "" && objective.value == ""){
        interest.required = true;
        objective.required = true;
    }
}

function sortRoadmaps(filtered, higher){
    var roadmapsList = document.getElementById(filtered+'Roadmaps');
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