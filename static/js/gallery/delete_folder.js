const deleteFolderRequest = new XMLHttpRequest();

function delete_folder(path, name) {
    let confirm = window.confirm("Are you sure you want to delete this folder?")
    if (!confirm) { return false; }
    deleteFolderRequest.open("POST", "/gallery/delete/folder/" + path + (path != "" ? "/" : "") + name + "/");
    deleteFolderRequest.send();
}

deleteFolderRequest.addEventListener("load", () => {
    location.reload();
});