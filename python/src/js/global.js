var playerAction = function(action, callback) {
	if( typeof callback === "undefined" ) {
		callback = function(d){ console.log(d); };
	}

	$.ajax({
		type: "POST",
		url: "index.html",
		data: { action: action }
	}).done(callback);
};

/*
var renderPlayerAction = function(action) {
	playerAction(action, function(info) {
		info = jQuery.parseJSON( info );
		var table = $("<table>");
		for( i in info ) {
			var row = $("<tr>")

			var label = $("<td>", { text:i } );
			var data = $("<td>", {text:info[i]} );

			table.append( row.append( data ) );
		}

		$("#info").empty().append( table );
	});
}
*/
