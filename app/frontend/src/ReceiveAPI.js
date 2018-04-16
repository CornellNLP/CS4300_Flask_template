import $ from 'jquery'

export var results = [];

export function getRelatedComments(input_query: string, callback) {
	console.log('running related comments fetch')
	$.get('http://0.0.0.0:5000/search', {query: input_query}).done(raw_data => {
		const data = JSON.parse(raw_data);
		console.dir(data);
		callback(data);
	}).fail((jqXHR, textStatus, errorThrown) => {
		console.log(errorThrown);
	})
}