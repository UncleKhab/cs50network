
d("#follow").addEventListener("click", () => {
    let followers = d('#followers')
    let following = d('#following')
    let button = d('#follow')

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