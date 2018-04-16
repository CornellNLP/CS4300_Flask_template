import $ from 'jquery'

export var results = [];

export function getRelatedComments(home: string) {
	console.log('running related comments fetch')
	const input_query = home.state.value
	$.get('http://0.0.0.0:5000/search', {query: input_query}).done(raw_data => {
		const data = JSON.parse(raw_data);
		results = data;
	}).fail((jqXHR, textStatus, errorThrown) => {
		console.log(errorThrown);
	})
}