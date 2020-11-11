
const fileinput = document.querySelector('input[type="file"]');
const reader = new FileReader();

function readFile() {

    reader.onload = function() {
        uploadData(btoa(reader.result));
    }
    reader.readAsBinaryString(fileinput.files[0]);
}

function uploadData(data) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/admin/blog/newpost/imageupload/", false);
    xhttp.send(data);

    var urlfield = document.getElementById("image-url");

    if (urlfield.innerHTML != "") {
        urlfield.innerHTML = "";
    }
    urlfield .innerHTML = xhttp.responseText;
}