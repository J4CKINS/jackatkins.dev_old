const deleteImageRequest = new XMLHttpRequest();

function delete_image(path, image) {
    let confirm = window.confirm("Are you sure you want to delete this image?")
    if (!confirm) { return false; }
    console.log((path != ("") ? "/":"") + path + image)
    deleteImageRequest.open("POST", "/gallery/delete/image" + (path != ("") ? "/":"") + path + image);
    deleteImageRequest.send();
}
deleteImageRequest.addEventListener("load", () => {
    location.reload();
});