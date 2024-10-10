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