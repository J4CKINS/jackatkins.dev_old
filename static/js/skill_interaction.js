const documentBody = document.getElementsByTagName("body");

function showDescription(event, text) {
    //find `la`st description box and delete it;
    deleteBox();
    var x = event.clientX;
    var y = event.clientY;

    let box = document.createElement("DIV");
    box.id = "description-box";
    box.innerHTML = text;
    
    document.getElementById("box-container").appendChild(box);
    expandAnimation(box);
}

function deleteBox() {
    let box = document.getElementById("description-box");
    if (box) { box.remove(); }
}

function expandAnimation(element) {
    let width = 0;
    let maxwidth = element.offsetWidth;

    element.style.width = "0px";

    let interval = setInterval(() => {
        if (element.offsetWidth < maxwidth) {
            width+=2;
            element.style.width = width + "px";
        }
        else {

            let windowWidth = Math.max(document.documentElement.clientWidth || 0, window.outerWidth || 0);
            
            if ((element.clientWidth + 10) > windowWidth) {
                element.style.width = "100%";
                element.style.whiteSpace = "normal"
            }
            clearInterval(interval);
        }
    }, 1);
}

// close skill description when window is clicked
// only delete the description box if a skill is not being clicked
window.addEventListener("click", (event) => {
    if (event.target.parentElement.id != "skill-icons") {
        deleteBox();
    }
});