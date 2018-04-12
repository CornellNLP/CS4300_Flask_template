$(document).ready(function() {
	var movies = $( "#movie_list" ).children();
	$('#similar_movies').on('input',function(e){
		var movie_list;
		var input_val = $('#similar_movies').val();
		if(input_val) {
			var ind = input_val.lastIndexOf(";");
			var filt;
			if(ind > -1) {
				var names = input_val.split(";");
				filt = names[names.length-1];
			}
			else{
				filt = input_val;
			}
			movie_list = movies.filter(function (i, d) {
				var name = d.value.toLowerCase();
				var index = name.indexOf(filt);
				if(index > -1){
					return true;
				}
				else {
					return false;
				}
			});
			console.log(movie_list);
			var list = document.getElementById("movie_list");
			list.innerHTML = '';
			movie_list.each(function(i, d) {
				var opt = document.createElement('option');
				opt.value = d.value;
    		list.appendChild(opt);
			});
		}
		else{
			movie_list = movies;
		}

	});

});
