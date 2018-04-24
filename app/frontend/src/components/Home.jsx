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
			loading : false
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
		let query = '?query=' + this.state.value
		event.preventDefault();
		this.props.history.push({
		  pathname: '/',
		  search: query
		})
		this.getRelatedComments(this.state.value)
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
				loading: false
			})
		})
	}

	render() {
		console.log(this.state.query.length)
		let data = this.state.data.filter(comment => { return comment.body !== "[deleted]"})
    return (
    	<div>
    		<div>
    			<div className="header">
		      <form>
		      	<label>
		      		<p className = "title">learnddit</p>
		      		<span>
		      		I want to learn how to...
		      		<input className="searchBar" id="search" type="text" value={this.state.value} onChange={this.handleChange} placeholder={this.suggestion}/>
		      		</span>
		      		<button id="submit_button" onClick={this.handleSubmit}><i className="fa fa-search fa-2x" aria-hidden="true"></i></button>
		      	</label>
		      </form>
		      {this.state.hasSearched && !this.state.query.length ? (<p> Similar terms: {this.state.query.map((term, i) => {
		      	return <span key={i}>{term[0]}</span>
		      })} </p>) : null}
		      </div>
		      <div>
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
