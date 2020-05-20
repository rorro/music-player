window.onload = function() {
    var song_list = [];
    var player = document.getElementById("player");

    player.setAttribute("src", localStorage.current_song);

    get_playlist();
}

function select_song(clicked) {
    let new_song = song_list[clicked.id];

    player.setAttribute("src", new_song);
    localStorage.setItem("current_song", new_song);
    player.play();
}

function get_playlist() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            song_list = JSON.parse(xhttp.response);

            if (localStorage.current_song === undefined) {
                localStorage.setItem("current_song", song_list[0]);
            }

            var ul = document.getElementById("lst");

            for (song in song_list) {
                let formatted_song = song_list[song].split("/").slice(2).join(" | ");
                formatted_song = formatted_song.split(".").slice(0,-1).join();

                let li = document.createElement("li");
                li.appendChild(document.createTextNode(unescape(formatted_song)));
                li.setAttribute("class", "playlist_entry");
                li.setAttribute("id", song);
                li.setAttribute("onclick", "select_song(this)");

                ul.appendChild(li);
            }
        }
    };

    xhttp.open("GET", "songlist", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}
