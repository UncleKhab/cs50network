


let followButton = document.getElementById('follow')
let likeButtons = document.querySelectorAll(".like-button");
let editButtons = document.querySelectorAll(".edit")
//-------------------------------------------------------------EVENT LISTENERS
if(likeButtons) {
    likeButtons.forEach(item => {
        item.addEventListener("click", like_handler);
    })
}
if(editButtons){
    editButtons.forEach(item =>{
        item.addEventListener("click", edit_handler)
    })
}

if(document.getElementById('post-form')){
    document.getElementById('post-form').addEventListener("submit", create_tweet)
}

if (followButton){
    followButton.addEventListener("click", () => {
        let followers = document.querySelector('#followers')
        let following = document.querySelector('#following')
        let button = document.querySelector('#follow')
    
        let user_id = button.getAttribute('data-user_id')
        
        fetch("/follow", {
            method:"POST",
            body: JSON.stringify({
                user_id: user_id,
            })
        })
        .then(response => response.json())
        .then(result => {
            followers.innerText = `Followers: ${result.followers}`;
            following.innerText = `Following: ${result.following}`;
            if(result.followed === true){
                button.innerText = 'Unfollow';
            } else {
                button.innerText = 'Follow';
            }
        })
    })
}


function like_handler(e) {
    
    let item = e.currentTarget;
    let item_id = item.getAttribute("data-id")
    let likes = item.querySelector("p")
    let icon = item.querySelector("img")

    fetch("/like",{
        method:"POST",
        body: JSON.stringify({
            id: item_id,
        })
    }).then(response => response.json())
      .then(response => {
          likes.innerText = response.likes;
          if (response.liked) {
            icon.setAttribute("src", "/static/network/icons/like-red.svg")
        } else {
            icon.setAttribute("src", "/static/network/icons/like.svg")
        }
      })
}

function edit_handler(e){
    let editButton = e.currentTarget
    let post_id = editButton.getAttribute('data-id')
    let content = document.getElementById(`tweet-content-${post_id}`).innerText;
    let contentContainer = document.getElementById(`tweet-content-${post_id}`).parentElement;

    contentContainer.innerHTML = editCreator(content, post_id);
    setHeight(`edit-text-${post_id}`)

    let editSend = document.getElementById("edit-send")
    let editCancel = document.getElementById("edit-cancel")
        editSend.addEventListener('click', ()=>{
            sendEdit(post_id, contentContainer)
        })
        editCancel.addEventListener('click', ()=>{
            contentContainer.innerHTML = pCreate(content, post_id)
        })
    }
function editCreator(content, post_id){
    return(
        `<textarea id="edit-text-${post_id}" class="edit-text" data-id="${post_id}">${content}</textarea>
        <button class="content-edit" id="edit-send">Edit</button>
        <button class="edit-cancel" id="edit-cancel">Cancel</button>`
        )
}
function setHeight(fieldId){
    document.getElementById(fieldId).style.height = document.getElementById(fieldId).scrollHeight+'px';
}
function pCreate(content, post_id){
    return(
        `
        <p id="tweet-content-${post_id}">
            ${content.trim()}
        </p>`
    )
}
function sendEdit(post_id, contentContainer){
    content = document.querySelector(".edit-text").value.trim();
    fetch("/edit", {
        method:"POST",
        body: JSON.stringify({
            post_id: post_id,
            edit_content: content,
        })
    })
    .then(response => response.json())
    .then(result => {
            if(result.error !== undefined){
                alert(result.error);
            } else {
                contentContainer.innerHTML = pCreate(content, post_id)
                
            }  
        })
}

function create_tweet(e){
    e.preventDefault()
    let content = document.getElementById('post-content').value;
    let status = 0;
    fetch('/create', {
        method:'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => {
        status = response.status;
        return response.json()
    })
    .then(response => {
        if(status === 201){
            
            location.reload()
        }else{
            alert(response.error)
        }
    })
}
