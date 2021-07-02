let createFolderRequest = new XMLHttpRequest();

function create_folder(path) {
    let name = prompt("Enter a folder name");
    if (name) {
        path = path + (path != "" ? "/" : "") + name;
        createFolderRequest.open("POST", "/gallery/new/folder/" + path + "/");
        createFolderRequest.send();
    }
    return;
}

createFolderRequest.addEventListener("load", () => {
    location.reload();
});