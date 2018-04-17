/*
	common JS across the site
*/

function getCSRF() {
	return document.cookie.split(";")
    .map((e) => {
        return (e.split("=")[0] == "csrftoken")? e.split("=")[1] : null;
    }).filter((e) => { return e; })[0];
};

/**
 * @description Converts a given Google MapAPI place to
 * the required JSON for storage
 * @param {JSON} place
 */
let placeToJSON = (place) => {
    let fields = ['address_components', 'vicinity', 'name', 'formatted_address', 'place_id'];
    let return_place = {};
    // commonplace field addition
    fields.forEach((v, i) => {
        return_place[v] = place[v];
    });
    // add the lat long details
    return_place['location'] = place.geometry.location.toJSON();
    return return_place;
};
