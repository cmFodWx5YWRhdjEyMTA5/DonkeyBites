/* Author:
khornberg
Testing client encryption - kinda of, maybe
*/

$("#submitButton").click(function(event) {
	// Change this to the encryption standard you want to us
	var hash = CryptoJS.SHA3($("#pwd").val());
	var data = "<br />User: " + $("#user").val() + " Hash: " + hash.toString(CryptoJS.enc.Hex);
	$("#results").append(data);
	event.preventDefault();
})
