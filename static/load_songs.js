window.onload = function() {
    var song_list = [];
    var song_list_len = 0;
    var player = document.getElementById("player");

    // first time listener
    if (localStorage.token === undefined) {
        let token = generate_token(18);

        localStorage.setItem("token", token);
        localStorage.setItem("current_song_index", 0);
        localStorage.setItem("current_song_link", "static/music/Janan%20Youkhanna/01-AudioTrack%2001.mp3");
    }

    // Pick up listening where you left off
    if (localStorage.current_song_link !== undefined) {
        let current_song_link = localStorage.current_song_link;

        player.setAttribute("src", current_song_link);
        player.load();
    }

    display_song_info();
    get_playlist();
}

function generate_token(length){
    var chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890".split("");
    var token = [];

    for (var i=0; i<length; i++) {
        var j = (Math.random() * (chars.length-1)).toFixed(0);
        token[i] = chars[j];
    }
    return token.join("");
}

function play_song(index) {
    let song_link = song_list[index];
    localStorage.setItem("current_song_link", song_link);
    localStorage.setItem("current_song_index", index);

    player.setAttribute("src", song_link);
    display_song_info();
    player.load();
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

function display_song_info() {
    let current_song_link = localStorage.current_song_link;
    let current_song_split = current_song_link.split("/");
    let song_index = current_song_split.length - 1;

    let current_singer = unescape(current_song_split[2]);
    let current_song = unescape(current_song_split[song_index].slice(0,-4));

    document.getElementById("current-singer").innerHTML = current_singer;
    document.getElementById("current-song").innerHTML = current_song;

    get_votes(current_song_link, localStorage.token);
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
                li.setAttribute("class", "playlist-entry");
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


function vote(up) {
    var data = {
        "link": localStorage.current_song_link,
        "token": localStorage.token
    }

    var xhttp = new XMLHttpRequest();
    if (up) {
        xhttp.open("POST", "vote", true);
        data["type"] = "up";
    }
    else {
        xhttp.open("POST", "vote", true);
        data["type"] = "down";
    }

    xhttp.setRequestHeader("Content-Type", "application/json");

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            display_votes(JSON.parse(xhttp.response));
        }
    }

    xhttp.send(JSON.stringify(data));
}

function display_votes(votes) {
    document.getElementById("thumb-up").innerHTML =  votes.upvotes;
    document.getElementById("thumb-down").innerHTML =  votes.downvotes;
}

function get_votes(link, token) {
    console.log(link);
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "votes", true);

    xhttp.setRequestHeader("token", token);
    xhttp.setRequestHeader("link", link);
    xhttp.setRequestHeader("Content-Type", "application/json");

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            display_votes(JSON.parse(xhttp.response));
        }
    }

    xhttp.send();
}
