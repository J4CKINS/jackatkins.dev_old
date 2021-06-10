const deleteImageRequest = new XMLHttpRequest();

function delete_image(path, image) {
    console.log((path != ("") ? "/":"") + path + image)
    deleteImageRequest.open("POST", "/delete/image" + (path != ("") ? "/":"") + path + image);
    deleteImageRequest.send();
}
deleteImageRequest.addEventListener("load", () => {
    location.reload();
});