async function loadBlogContent(id) {

    // Get elements
    let post = document.getElementById(`blog-${id}`);
    let post_content = post.getElementsByClassName('post-content')[0];
    let expand_button = post.getElementsByClassName('expand')[0];

    // Check if post content is empty
    if (post_content.innerHTML == "") {
        fetch(`./${id}/?raw_content=true`) // Fetch post content
            .then(response => {
                // If request was successful
                if (response.status == 200) { 
                    response.text().then(data => {
                        post_content.innerHTML = data; // Set content field with post content data
                        expand_button.innerHTML = "Show Less" // Change expand button
                    })
                }
                // Request unsuccessful
                else {
                    console.error(`AN ERROR OCCURED: ${reason}`);
                }
            })
            // Fetch error
            .catch(reason => {
                console.error(`AN ERROR OCCURED: ${reason}`)
            });
    }
    else {
        // Remove all post content
        post_content.innerHTML = "";
        expand_button.innerHTML = "Show More" // Revert expand button to original text
    }
}