function copy_to_clipboard(id) {
    let row = document.getElementById(id);
    let copyArea = row.querySelector('#copy-buffer');
    copyArea.type = "text" // input needs to be shown to be selected
    copyArea.select();
    document.execCommand('copy');
    copyArea.type = "hidden" // hide the input element again
}