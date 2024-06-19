function likeClicked() {
    let id = sessionStorage.getItem('current')      

    fetch('/addClicked', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: id            //this was stored as a JSON, no need to convert
    })
    .then(response => response.json())  
    .then(data => console.log(data))  
    .catch(error => console.error(error));

    loadInfo();
    location.reload();
}

function dislikeClicked(){
    loadInfo()
    location.reload();
}

function loadInfo(){
    fetch('/loadNext')
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem('current', JSON.stringify({id : data.id}))   //storing the id to use later in likeClicked

        document.getElementById("r_Name").textContent = data.name;
        document.getElementById("r_Desc").textContent = data.cuisine_type;
        img = document.getElementById("r_Img")
        img.addEventListener("error", function(event) {
            event.target.src = "/static/images/No-Image-Placeholder.svg.png"
            event.onerror = null
        })
        img.src = data.estabImg;
    }).catch(error => console.error(error))
}