function d(selector){
    return document.querySelector(selector);
}

let like = document.querySelectorAll(".liked");
let edit = document.querySelectorAll(".edit");

//-------------------------------------------------------------EVENT LISTENERS
document.getElementById('post-form').addEventListener("submit", create_tweet)


edit.forEach((element) => {
    edit_handler(element);
});

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
                like_button.innerHTML = '<i class="far fa-heart icon"></i>';
            } else {
                like_button.innerHTML = '<i class="fas fa-heart icon"></i>';
            }
        })
    })
}

function edit_handler(element){
    element.addEventListener("click", () => {
        let post_id = element.getAttribute("data-post_id")
        let content_container = d(`#content_container_${post_id}`)
        let content = d(`#post_content_${post_id}`)
        let button = d(`#edit_button_${post_id}`)
        
        if (button.innerText === "Edit"){
            let input = document.createElement('span')
            input.setAttribute("id", `post_input_${post_id}`);
            input.setAttribute("role", "textbox");
            input.setAttribute("class", 'edit-content-field');
            input.setAttribute("contenteditable", "");
            input.setAttribute("spellcheck", "false");
            input.innerText = content.innerText;
            content.innerText = "";
            content.style.border = "1px solid #00adff";
            content.append(input);
            d(`#post_input_${post_id}`).focus()
            
            button.innerText = "Save"
        } else {
            let edit_content = d(`#post_input_${post_id}`).innerText
            fetch("/edit", {
                method:"POST",
                body: JSON.stringify({
                    post_id: post_id,
                    edit_content: edit_content,
                })
            })
            .then(response => response.json())
            .then(result => {
                if(result.error !== undefined){
                    alert(result.error);
                } else {
                    content.innerText = edit_content
                    content.style.border = "none"
                    button.innerText = "Edit"
                }  
            })
            }
        
        
    })
}
function create_tweet(e){
    e.preventDefault()
    let content = document.getElementById('post-content').value;

    fetch('/create', {
        method:'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        location.reload()
    })
}
// function create_post(){
//     d('#post-form').onsubmit = function() {
//         let content = d('#post-content').value;

//     fetch('/create', {
//         method: 'POST',
//         body: JSON.stringify({
//             content: content,
//         })
//     })
//     .then(response => response.json())
//     .then(result => {
//         if(result.error !== undefined){
//             alert(result.error);
//         }
//         else
//         {
//             location.reload();
//         }
//     });
//     return false;
//     }
// }
// create_post();


// d("#follow").addEventListener("click", () => {
//     let followers = d('#followers')
//     let following = d('#following')
//     let button = d('#follow')

//     let user_id = button.getAttribute('data-user_id')
    
//     fetch("/follow", {
//         method:"POST",
//         body: JSON.stringify({
//             user_id: user_id,
//         })
//     })
//     .then(response => response.json())
//     .then(result => {
//         followers.innerText = `Followers: ${result.followers}`;
//         following.innerText = `Following: ${result.following}`;
//         if(result.followed === true){
//             button.innerText = 'Unfollow';
//         } else {
//             button.innerText = 'Follow';
//         }
//     })
// })