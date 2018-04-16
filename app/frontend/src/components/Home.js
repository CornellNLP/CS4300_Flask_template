import React, { Component } from 'react';
import getRelatedComments from '../ReceiveAPI.js'

class Home extends Component {
	constructor(props){
		super(props);
		this.state = {value: ''};

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
		getRelatedComments(this.state.value)
	}



	render() {
	    return (
	      <form>
	      	<label>
	      		<p class = "title">LEARNDDIT</p>
	      		<input className = "searchBar" type="text" value={this.state.value} onChange={this.handleChange} />
	      		<button id = "submit_button" onClick={this.handleSubmit}>Search</button>
	      	</label>
	      	
	      </form>
	    );
	}
}

export default Home;
