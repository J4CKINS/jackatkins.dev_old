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