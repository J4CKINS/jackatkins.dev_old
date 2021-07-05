function showDescription(event, text) {
    //find last description box and delete it;
    deleteBox();
    clearClickedStyle();
    
    // get element that has been clicked
    let target = event.target;
    target.classList.add("clicked")

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

function clearClickedStyle() {
    // Removes all clicked classes from buttons
    let buttons = document.getElementById("skill-icons").children;
    for(let x = 0; x < buttons.length; x++) {
        buttons[x].classList.remove("clicked");
    }
}

// close skill description when window is clicked
// only delete the description box if a skill is not being clicked
window.addEventListener("click", (event) => {
    try {
        if (event.target.parentElement.id != "skill-icons") {
            clearClickedStyle();
            deleteBox();
        }
    }
    catch {
        
    }
});