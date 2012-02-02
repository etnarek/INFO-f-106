function new_thread_box(doc, page) {
	overlay_reset();
	overlay_title("New Thread");
	overlay_show();
	$('#overlay_content').load('/note/new_thread/' + doc + '/' + page, overlay_refresh);
}

function list_thread(course, doc, page) {
	overlay_reset();
	overlay_title("Thread about the page " + page);
	overlay_show();
	$('#overlay_content').load('/note/list_thread/' + course + '/' + doc + '/' + page, overlay_refresh);
}

function preview_thread(id, place) {
	if ($('#prev' + id).length > 0)
		return;
	$('#' + place).after('<tr><td class="min2"></td><td colspan=2><div id="prev'+id+'">loading..</div></td></tr>');
	$('#prev' + id).load('/note/prev_thread/' + id, overlay_refresh);
}
