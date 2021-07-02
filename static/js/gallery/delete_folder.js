const deleteFolderRequest = new XMLHttpRequest();

function delete_folder(path, name) {
    deleteFolderRequest.open("POST", "/gallery/delete/folder/" + path + (path != "" ? "/" : "") + name + "/");
    deleteFolderRequest.send();
}

deleteFolderRequest.addEventListener("load", () => {
    location.reload();
});