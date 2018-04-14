popup_ids = ["donations", "tweets", "votes"]

function showPopup(show_id) {
	for (id of popup_ids) {
		document.getElementById(id).style.display = "none";
	}
	document.getElementById(show_id).style.display = "block";
}