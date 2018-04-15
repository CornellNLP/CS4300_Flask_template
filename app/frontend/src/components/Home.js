import React, { Component } from 'react';

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
		alert('Your search was: ' + this.state.value);
		event.preventDefault();
	}



	render() {
	    return (
	      <form onSubmit = {this.handleSubmit}>
	      	<label>
	      		<input className = "searchBar" type="text" value={this.state.value} onChange={this.handleChange} />
	      		<input type="submit" value="Search"/>
	      	</label>
	      	
	      </form>
	    );
	}
}

export default Home;
