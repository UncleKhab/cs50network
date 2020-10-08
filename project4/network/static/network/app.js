function d(selector){
    return document.querySelector(selector);
}

let like = document.querySelectorAll(".liked");

like.forEach((element) => {
    like_handler(element);
});


function like_handler(element) {
    element.addEventListener("click", () =>{
        
        let id = element.getAttribute("data-post_id")
        let like_count = d(`#like_count_${id}`)
        let like_button = d(`#like_button_${id}`)
        
        fetch("/like", {
            method:"POST",
            body: JSON.stringify({
                id: id,
            })
        })
        .then(response => response.json())
        .then(result => {
            like_count.innerText = result.likes
            if (result.liked === false){
                like_button.innerText = 'Like';
            } else {
                like_button.innerText = 'Unlike';
            }
        })
    })
}