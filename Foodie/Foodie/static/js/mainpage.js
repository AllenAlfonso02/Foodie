function likeClicked(restaurant) {
    const restaurantData = {
        restaurant_id: restaurant.id  // Assuming you have the restaurant ID
    };

    fetch('/addClicked', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(restaurantData)
    })
    .then(response => response.json())  // parse response
    .then(data => console.log(data))  // do something with parsed data
    .catch(error => console.error(error));

    loadInfo();
    location.reload();
}

function dislikeClicked(){
    loadInfo()
    location.reload()
}

function loadInfo(){
    fetch('/loadNext')
    .then(response => response.json())
    .then(data => {
        document.getElementById("r_Name").textContent = data.name;
        document.getElementById("r_Desc").textContent = data.description;
        img = document.getElementById("r_Img")
        img.addEventListener("error", function(event) {
            event.target.src = "/static/images/No-Image-Placeholder.svg.png"
            event.onerror = null
        })
        img.src = data.picture;
    }).catch(error => console.error(error))
}