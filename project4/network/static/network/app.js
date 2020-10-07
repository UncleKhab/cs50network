// HELPER FUNCTIONS
// 1. Query Selector
function d(selector){
    return document.querySelector(selector);
}

// 2. 

//------------------------------------------------------------------------------------Functionality

function create_post(){
    d('#post-form').onsubmit = function() {
        let content = d('#post-content').value;
    

    fetch('/create', {
        method: 'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => response.json())
    .then(result => {
        if(result.message === "Post created successfully."){
            alert(result.message);
        } else {
            alert(result.error)
            return false;
        }
    });
    return false;
    }
}
create_post();