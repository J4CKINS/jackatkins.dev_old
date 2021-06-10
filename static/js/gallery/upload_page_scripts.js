function file_selected() {
    let fileElement = document.getElementById('file');
    let filenameElement = document.getElementById('filename');
    let formatElement = document.getElementById('format');

    let image_preview = document.getElementById('image-preview');

    let file = fileElement.files[0];
    if (file) {
        image_preview.src = URL.createObjectURL(file); // set image preview
        filenameElement.value = file.name.split(".")[0];
        formatElement.value = file.name.split(".")[1];
    }
}

function select_image() {
    let fileElement = document.getElementById('file');
    fileElement.click();
}