import $ from 'jquery'

export function getRelatedComments(input_query: string) {
	console.log('running related comments fetch')
	$.get('http://0.0.0.0:5000/search', {query: input_query}).done(data => {
		console.dir(data);
	}).fail((jqXHR, textStatus, errorThrown) => {
		console.log(errorThrown);
	})
}