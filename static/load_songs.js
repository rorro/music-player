window.onload = function() {
    var song_list = [];
    var song_list_len = 0;
    var player = document.getElementById("player");

    if (localStorage.current_song_link !== undefined) {
        player.setAttribute("src", localStorage.current_song_link);
        player.load()
    }

    get_playlist();
}

function play_song(index) {
    let song_link = song_list[index];
    localStorage.setItem("current_song_link", song_link);
    localStorage.setItem("current_song_index", index);

    player.setAttribute("src", song_link);
    player.load()
    player.play();
}

function select_song(clicked) {
    play_song(clicked.id);
}

function play_next() {
    let current_song_index = parseInt(localStorage.current_song_index);
    if (current_song_index < song_list_len) {
        let next_song_index = current_song_index + 1;
        play_song(next_song_index);
    }
}

function play_previous() {
    let current_song_index = parseInt(localStorage.current_song_index);
    if (current_song_index > 0) {
        let previous_song_index = current_song_index - 1;
        play_song(previous_song_index);
    }
}

function get_playlist() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            song_list = JSON.parse(xhttp.response);
            song_list_len = song_list.length - 1;

            if (localStorage.current_song_link === undefined) {
                localStorage.setItem("current_song_link", song_list[0]);
                localStorage.setItem("current_song_index", 0);
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
