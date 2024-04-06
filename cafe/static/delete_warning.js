function warningMessage() {
    let result = confirm("Na pewno chcesz usunąć to?");
    return result;
}

document.addEventListener("DOMContentLoaded", function() {
    let deleteLinks = document.querySelectorAll(".delete_link");
    deleteLinks.forEach(function (link) {
        link.addEventListener("click", function (event){
            event.preventDefault();
            let result = warningMessage();
            if (result) {
                window.location.href = link.getAttribute("href");
            }
        });
    });
});