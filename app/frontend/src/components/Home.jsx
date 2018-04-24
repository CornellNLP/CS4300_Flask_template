import React, { Component } from 'react';
import axios from 'axios'
import queryString from 'query-string'

import Result from './Result'

class Home extends Component {
	constructor(props){
		super(props);
		this.state = {
			value: '',
			data : [],
			query: [],
			hasSearched: false,
			loading : false,
			errored: false,
		};
		const randSuggestions = ["play the piano", "motivate myself", "sleep earlier", "be less insecure", "speak japanese"]
    this.suggestion = randSuggestions[Math.floor(Math.random()*randSuggestions.length)]

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.getRelatedComments = this.getRelatedComments.bind(this)
		this.getRelatedSearchTerms = this.getRelatedSearchTerms.bind(this)
	}

	componentWillMount(){
		console.log(this.props)
		let query = this.props.location.search
		if (query) {
			let parsed = queryString.parse(query)
			this.getRelatedComments(parsed.query)
			this.setState({value: parsed.query})
		}
	}

	handleChange(event){
		this.setState({value: event.target.value});
	}

	handleSubmit(event){
		let submission = this.state.value === "" ? this.suggestion : this.state.value
		let query = '?query=' + submission
		event.preventDefault();
		this.props.history.push({
		  pathname: '/',
		  search: query
		})
		this.getRelatedComments(submission)
	}

	getRelatedSearchTerms(input_query) {
		var arr = input_query.split(" ")
		var qParams = arr.map(key =>key).join('&');
		console.log('running related query fetch')
		axios.get('/svd', {
				params: { query: qParams }
			})
		.then(response => {
			console.log(response)
			this.setState({
				query : response.data
			})
		})
	}

	getRelatedComments(input_query) {
		if(input_query === "") {
			input_query = this.suggestion;
		}
		this.setState({loading: true})
		var arr = input_query.split(" ")
		var qParams = arr.map(key =>key).join('&');
		console.log('running related comments fetch')
		axios.get('/search', {
				params: { query: qParams }
			})
		.then(response => {
			this.getRelatedSearchTerms(input_query)
			console.log(response)
			this.setState({
				data: response.data,
				hasSearched: true,
				loading: false,
				errored: false
			})
		}).catch(error => {
			this.setState({ errored: true });
			console.error(error);
		});
	}

	render() {
		let data = this.state.data.filter(comment => { return comment.body !== "[deleted]"})
		let terms = this.state.query.map((term, i) => { return term[0] });
  	terms = Array.from(new Set(terms));
  	console.log(terms)
  	let termList = terms.join(", ");
    return (
    	<div>
    		<div>
    			<div className="header">
		      <form>
		      	<label>
		      		<p className = "title">learnddit</p>
		      		{this.state.errored ? <div className="alert alert-danger">Failed to retrieve results!</div> : null}
		      		<span>
		      		I want to learn how to...
		      		<input className="searchBar" id="search" type="text" value={this.state.value} onChange={this.handleChange} placeholder={this.suggestion}/>
		      		</span>
		      		<button id="submit_button" onClick={this.handleSubmit}><i className="fa fa-search fa-2x" aria-hidden="true"></i></button>
		      	</label>
		      </form>
		      </div>
		      <div>
		      {this.state.hasSearched && this.state.query.length ? (<div className="related"> Similar terms: { termList } </div>) : null}
		      {
		      	this.state.loading ? (<div className="loader"></div>) :
		      	(data.map((comment, i) => {
		      		return <Result key={comment.id} comment={comment} style={i % 2 === 0 ? "white" : "whitesmoke"}/>
		      	}))
		      }
	      </div>
	      </div>
	    	<div className="footer">
	    		<p>Zack Brody (ztb5), Eric Feng (evf23), Michelle Ip (mvi4), Monica Ong (myo3), Jill Wu (jw975)</p>
	    		<p>A project for Cornell's <a href="http://www.cs.cornell.edu/courses/cs4300/2018sp/" target="_blank"> CS 4300</a></p>
	    	</div>
      </div>
	    );
	}
}

export default Home;
