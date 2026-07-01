let scores = {};
let reconnect_in = 0;

function draw_map() {
    map = new jvm.Map({
        container: $("#world_map"),
        map: "world_mill",
        zoomOnScroll: false,
        backgroundColor: "transparent",
        regionStyle: {
            initial: {
                fill: "#6c757d",
                "fill-opacity": 0.9,
                stroke: "none",
                "stroke-width": 0,
                "stroke-opacity": 1,
            },
            hover: {
                "fill-opacity": 0.8,
                cursor: "default",
            },
        },
        series: {
            regions: [
                {
                    values: scores,
                    scale: ["#C8EEFF", "#0071A4"],
                    normalizeFunction: "polynomial",
                    min: 0,
                    max: 0,
                },
            ],
        },
        onRegionTipShow: function (e, el, code) {
            if (scores[code]) {
                el.html(el.html() + " (" + scores[code] + " events)");
            } else {
                el.html(el.html());
            }
        },
    });
}

function max_from_scores() {
    let max = 0;
    for (key in scores) {
        if (scores[key] > max) {
            max = scores[key];
        }
    }
    return max;
}

function redraw_map() {
    map.series.regions[0].setValues(scores);
    map.series.regions[0].params.max = max_from_scores();
}

function get_ws_url() {
    let proto = window.location.protocol === "https:" ? "wss://" : "ws://";
    let host = window.location.hostname;
    let port = "";
    if (host != window.location.host) {
        // the application uses a custom port
        port = ":" + ws_port;
    }
    let path = "/ws";
    return proto + server + port + path;
}

function ws_onopen(event) {
    $("#status_status").html("Socket opened, waiting for data...");
}

function ws_onmessage(event) {
    let msg = JSON.parse(event.data);

    switch (msg.msgtype) {
        case "info":
            $("#status_status").html(msg.payload.msg);
            break;
        case "dynfw delta":
            handle_delta(msg.payload);
            break;
        case "dynfw list":
            handle_list(msg.payload);
            break;
        case "dynfw event":
            handle_event(msg.payload);
            break;
        default:
            $("#status_status").html("Received unknown message");
            break;
    }
}

function ws_onclose(event) {
    $("#status_status").html(
        `Disconnected - trying to reconnect (in ${reconnect_in / 1000}s)`
    );
    setTimeout(function () {
        ws_connect();
    }, reconnect_in);

    if (reconnect_in < 10000) {
        reconnect_in += 1000;
    }
}

function ws_connect() {
    let socket = new WebSocket(get_ws_url());

    socket.onopen = ws_onopen;
    socket.onclose = ws_onclose;
    socket.onmessage = ws_onmessage;
}

$(document).ready(function () {
    ws_connect();
    draw_map();

    $("#expand_list").on("click", function () {
        list_shown += LIST_PAGE_SIZE;
        render_list();
    });
    $("#collapse_list").on("click", function () {
        list_shown = LIST_PAGE_SIZE;
        render_list();
    });
    $("#list_filter").on("input", function () {
        list_filter = $(this).val().trim();
        // Each new filter starts from the first page of matches.
        list_shown = LIST_PAGE_SIZE;
        render_list();
    });
});

function handle_delta(msg) {
    if (msg.delta == "positive") {
        $("#latest_data").prepend(
            `<li class="list-group-item list-group-item-action list-group-item-danger"><i class="fas fa-plus mr-1"></i>${msg.ip}</li>`
        );
    } else {
        $("#latest_data").prepend(
            `<li class="list-group-item list-group-item-action list-group-item-success"><i class="fas fa-minus mr-1"></i>${msg.ip}</li>`
        );
    }
    if ($("#latest_data li").length >= 30) {
        $("#latest_data li").last().remove();
    }
}

// Number of list rows shown per page (matches the Events list cap, minus one for button row and one more to match other lists).
const LIST_PAGE_SIZE = 28;
// Full current list as last received from the server.
let list_data = [];
// Active filter substring; only IPs containing it are listed.
let list_filter = "";
// How many of the (filtered) rows are currently rendered; preserved across
// refreshes so an expanded view does not collapse when the list is refreshed
// periodically.
let list_shown = LIST_PAGE_SIZE;

function filtered_list() {
    if (!list_filter) {
        return list_data;
    }
    return list_data.filter((ip) => ip.includes(list_filter));
}

function render_list() {
    let matches = filtered_list();
    let shown = Math.min(list_shown, matches.length);
    let items = "";
    for (let i = 0; i < shown; i++) {
        items += `<li class="list-group-item list-group-item-action list-group-item-light">${matches[i]}</li>`;
    }
    if (matches.length === 0) {
        items =
            '<li class="list-group-item list-group-item-light text-muted">No matching IPs</li>';
    }
    $("#latest_list").html(items);

    // Badge shows the match count vs. total when filtering, total otherwise.
    $("#list_cnt").html(
        list_filter ? `${matches.length} / ${list_data.length}` : list_data.length
    );

    let expand_hidden = shown >= matches.length;
    let collapse_hidden = list_shown <= LIST_PAGE_SIZE;
    $("#expand_list").toggleClass("d-none", expand_hidden);
    $("#collapse_list").toggleClass("d-none", collapse_hidden);
    // Hide the controls container entirely when no button is shown, so its
    // padding doesn't add empty space below the list. Toggle d-flex/d-none
    // together: with both present d-flex wins over d-none in Bootstrap's CSS.
    let controls_hidden = expand_hidden && collapse_hidden;
    $("#list_controls")
        .toggleClass("d-none", controls_hidden)
        .toggleClass("d-flex", !controls_hidden);
    // Apply the gap only when both buttons are visible, otherwise it adds
    // extra space next to the single full-width button.
    $("#list_controls").css("gap", !expand_hidden && !collapse_hidden ? "0.5rem" : "");
}

function handle_list(msg) {
    list_data = msg.list;
    let d = new Date(msg.ts * 1000);
    $("#status_updated").html(d.toUTCString());
    $("#status_list_version").html(msg.version);
    $("#status_serial").html(msg.serial);
    render_list();
}

function handle_event(msg) {
    let item = `<li class="list-group-item list-group-item-action list-group-item-warning"> `;
    if (msg.geo) {
        item += `<span class="fi fi-${msg.geo.toLowerCase()}"></span> `;
    } else {
        item += `<span class="fi fi-xx"></span> `;
    }
    item += `${msg.ip} `;
    item += `<span class="badge badge-secondary">${msg.event}</span> `;
    item += `</li>`;

    $("#latest_event").prepend(item);
    if ($("#latest_event li").length >= 30) {
        $("#latest_event li").last().remove();
    }

    if (msg.geo) {
        if (!scores[msg.geo]) {
            scores[msg.geo] = 0;
        }
        scores[msg.geo] += 1;
    }
    redraw_map();
}
