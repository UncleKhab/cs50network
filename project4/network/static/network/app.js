like = document.querySelectorAll(".liked");

like.forEach((element) => {
    like_handler(element);
});


function like_handler(element) {
    element.addEventListener("click", () =>{
        
        id = element.getAttribute("data-post_id")
        like_count = document.querySelector(`#like_count_${id}`)
        like_button = document.querySelector(`#like_button_${id}`)
        like_button_text = like_button.innerText
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