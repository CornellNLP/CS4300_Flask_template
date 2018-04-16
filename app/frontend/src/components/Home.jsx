import React, { Component } from 'react';
import { getRelatedComments, results } from '../ReceiveAPI.js'
import $ from 'jquery'

class Home extends Component {
	constructor(props){
		super(props);
		this.state = {value: '', results: []};

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(event){
		this.setState({value: event.target.value});
	}

	handleSubmit(event){
		//putting an alert for now, should instead send api request on submit
		// if (this.state.value == ""){
		// 	alert('Empty Search Query');
		// }else{
		// 	alert('Your search was: ' + this.state.value);
		// }
		event.preventDefault();
		getRelatedComments(this);
	}



	render() {
	    return (
			<div>
				<form>
				<label>
					<p className = "title">LEARNDDIT</p>
					<input className = "searchBar" type="text" value={this.state.value} onChange={this.handleChange} />
					<button id = "submit_button" onClick={this.handleSubmit}>Search</button>
				</label>
			
				</form>
				<div id = "results_section">
					{
						this.state.results.map(result => {
							<Result body={result.body} />
						})
					}
				</div>
			</div>
	    );
	}
}

export default Home;
