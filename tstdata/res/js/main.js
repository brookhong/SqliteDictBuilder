document.addEventListener('DOMContentLoaded', function (e) {
    var fayin = document.querySelectorAll("a.fayin");
    if (fayin.length) {
        var audio = document.createElement("audio");
        document.body.firstElementChild.append(audio);
        fayin.forEach(function(d) {
            d.onclick = function (evt) {
                audio.src = d.href;
                audio.play();
                evt.preventDefault();
            };
        });
    }
});
