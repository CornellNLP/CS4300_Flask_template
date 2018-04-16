import axios from 'axios'

export function getRelatedComments(input_query) {
	var arr = input_query.split(" ")
	console.log('running related comments fetch')
	axios.get('http://0.0.0.0:5000/search', {
			params: { arr }
		})
	.then(response => console.log(response))


	// $.get(, {query: input_query}).done(data => {
	// 	console.dir(data);
	// }).fail((jqXHR, textStatus, errorThrown) => {
	// 	console.log(errorThrown);
	// })
}