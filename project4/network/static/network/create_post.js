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
        if(result.error !== undefined){
            alert(result.error);
        }
        else
        {
            location.reload();
        }
    });
    return false;
    }
}
create_post();