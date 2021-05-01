function setExpandControls() {
    const max_height = 500;
    var posts = document.getElementsByClassName("post-container");
    for (let element of posts) {
        let expand = element.getElementsByClassName("expand")[0]
        let post_object = element.getElementsByClassName("post")[0];
        if(element.offsetHeight < max_height) {
            // delete expand element as it is not needed
            expand.remove();
        }
        else {
            post_object.style.height = max_height.toString() + "px"
        }
    }
}

function expand(id) {
    
    var post = document.getElementById("blog-" + id);
    var text = document.getElementById("expand-" + id);

    if (post.style.height === "auto") {
        post.style.height = "500px";
        text.innerText = "Show More";
    }
    else {
        post.style.height = "auto";
        text.innerText = "Show Less"
    }
}