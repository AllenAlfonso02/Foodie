function likeClicked() {
    let restaurant = {
        id: sessionStorage.getItem('currentID'),
        name: document.getElementById("r_Name").textContent,
        description: document.getElementById("r_Desc").textContent,
        estabImg: document.getElementById("r_Img").src
    };

    fetch('/addClicked', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(restaurant)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

    loadInfo();
    location.reload();
}

function dislikeClicked(){
    loadInfo();
    location.reload();
}

function loadInfo() {
    fetch('/loadNext')
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem('currentID', data.id);
        document.getElementById("r_Name").textContent = data.name;
        document.getElementById("r_Desc").textContent = data.description;
        let img = document.getElementById("r_Img");
        img.addEventListener("error", function(event) {
            event.target.src = "/static/images/No-Image-Placeholder.svg.png";
            event.onerror = null;
        })
        img.src = data.picture;
    }).catch(error => console.error(error));
}
