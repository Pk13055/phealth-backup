/*
	common JS across the site
*/

function getCSRF() {
	return document.cookie.split(";")
    .map((e) => {
        return (e.split("=")[0] == "csrftoken")? e.split("=")[1] : null;
    }).filter((e) => { return e; })[0];
};
