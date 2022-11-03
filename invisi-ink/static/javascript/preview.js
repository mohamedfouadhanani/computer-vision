let button = document.getElementById("preview");

button.onclick = (event) => {
	event.preventDefault();

	form = document.getElementById("form");

	form.action = "/preview/";
	form.target = "_blank";

	form.submit();

	form.action = "/encode/";
	form.target = "_parent";
};
