let scores = {};
let reconnect_in = 0;


function draw_map() {
	map = new jvm.Map({
		container: $('#world_map'),
		map: 'world_mill',
		series: {
			regions: [{
				values: scores,
				scale: ['#C8EEFF', '#0071A4'],
				normalizeFunction: 'polynomial',
				min: 0,
				max: 0
			}]
		},
		onRegionTipShow: function(e, el, code){
			if (scores[code]) {
				el.html(el.html()+' ('+scores[code]+' events)');
			} else {
				el.html(el.html());
			}
		}
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
	if (host == window.location.host) {
		let port = ":" + ws_port;
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
	$("#status_status").html(`Disconnected - trying to reconnect (in ${reconnect_in/1000}s)`);
	setTimeout(function(){
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

$(document).ready(function(){
	ws_connect();
	draw_map();
})

function handle_delta(msg) {
	if (msg.delta == "positive") {
		$('#latest_data').prepend(`<li class="list-group-item list-group-item-success"><span class="oi oi-plus mr-1"></span> ${msg.ip}</li>`);
	} else {
		$('#latest_data').prepend(`<li class="list-group-item list-group-item-danger"><span class="oi oi-minus mr-1"></span> ${msg.ip}</li>`);
	}
	if ($('#latest_data li').length >= 30) {
		$('#latest_data li').last().remove()
	}
};

function handle_list(msg) {
	let items = "";
	for (let i in msg.list) {
		items = items + `<li class="list-group-item">${msg.list[i]}</li>`;
	}
	let d = new Date(msg.ts*1000)
	$('#latest_list').html(items);
	$('#status_updated').html(d.toUTCString());
	$('#status_list_version').html(msg.version);
	$('#status_serial').html(msg.serial);
	$('#list_cnt').html(msg.list.length);
};

function handle_event(msg) {
	let item = `<li class="list-group-item list-group-item-warning"> `;
	if (msg.geo) {
		item += `<span class="badge badge-primary"><samp>${msg.geo}</samp></span> `
	} else {
		item += `<span class="badge badge-primary"><samp>??</samp></span> `
	}
	item += `${msg.ip} `;
	item += `<span class="badge badge-secondary">${msg.event}</span> `
	item += `</li>`

	$('#latest_event').prepend(item);
	if ($('#latest_event li').length >= 30) {
		$('#latest_event li').last().remove()
	}

	if (msg.geo) {
		if (!scores[msg.geo]) {
			scores[msg.geo] = 0;
		}
		scores[msg.geo] += 1;
	}
	redraw_map();
};
