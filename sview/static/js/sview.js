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

function check_status(url, data, success, error) {
	$.ajax({
		method: "POST",
		url: url,
		data: data,
		success: success,
		error: error
	});
}
