var showText = function (target, message, index, interval) {   
  if (index < message.length) {
    target.innerHTML += message[index++];
    setTimeout(function () { showText(target, message, index, interval); }, interval);
  }
}


function startAnimation () {
    const title = document.getElementById("page-title");
    title.style.color = "#27ae60";
    showText(title, "\"Hello, World!\"", 0, 70);  
}
