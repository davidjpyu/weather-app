var modal = document.getElementById("info-modal");
var btn = document.getElementById("info-btn");
var span = document.getElementsByClassName("close")[0];

// clicks the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// clicks on (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// clicks outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
