function draw_map(elem_handler, scores) {
	$(elem_handler).vectorMap({
		map: 'world_mill',
		series: {
			regions: [{
				values: scores,
				scale: ['#C8EEFF', '#0071A4'],
				normalizeFunction: 'polynomial'
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

function await_job(url, job_id) {
	window.setInterval(await_job_poll, 1000, url, job_id);
}

function await_job_poll(url, job_id) {
	$.ajax({
		method: "POST",
		url: url,
		data: {"job_id": job_id},
		success: await_job_success,
		error: await_job_error
	});
}

function await_job_success(data) {
	if ("job_done" in data) {
		if (data["job_done"] == true) {
			window.location.reload();
		}
	}
}

function await_job_error(data) {
	$("#await_job_alert").html(data.responseJSON["error"]);
	$("#await_job_alert").removeClass("d-none").addClass("d-block");
	$("#await_job_spinner").addClass("d-none").removeClass("d-block");
}
