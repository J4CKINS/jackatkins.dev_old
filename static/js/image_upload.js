
const fileinput = document.querySelector('input[type="file"]');
const reader = new FileReader();

function readFile(url) {

    reader.onload = function() {
        uploadData(btoa(reader.result), url);
    }
    reader.readAsBinaryString(fileinput.files[0]);
}

function uploadData(data, url) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/admin/imageupload/", false);
    xhttp.send(data);

    var urlfield = document.getElementById("image-url");

    if (urlfield.innerHTML != "") {
        urlfield.innerHTML = "";
    }
    urlfield .innerHTML = xhttp.responseText;
}