// Auto-dismiss flash messages after a few seconds
document.addEventListener("DOMContentLoaded", function () {
    const flashes = document.querySelectorAll(".flash");
    flashes.forEach(function (el) {
        setTimeout(function () {
            el.style.transition = "opacity 0.5s ease";
            el.style.opacity = "0";
            setTimeout(function () {
                el.remove();
            }, 500);
        }, 5000);
    });
});
