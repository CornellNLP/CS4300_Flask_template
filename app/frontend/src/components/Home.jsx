import React, { Component } from 'react';
import axios from 'axios'
import queryString from 'query-string'

import Result from './Result'

const DEFAULT_NUM = 10;

class Home extends Component {
	constructor(props){
		super(props);
		this.state = {
			value: '',
			data : [],
			numShowing: DEFAULT_NUM,
			hasSearched: false,
			loading : false,
			errored: false,
			start_index: 0
		};
		const randSuggestions = ["play the piano", "motivate myself", "sleep earlier", "be less insecure", "speak japanese"]
    this.suggestion = randSuggestions[Math.floor(Math.random()*randSuggestions.length)]

    this.showMore = this.showMore.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.getRelatedComments = this.getRelatedComments.bind(this);
	}

	componentWillMount(){
		console.log(this.props)
		let query = this.props.location.search
		console.dir(this.props)
		let input_index = this.props.history.start_index
		if (query) {
			let parsed = queryString.parse(query)
			if (parsed.input_index) this.setState({start_index: parsed.input_index})
			this.getRelatedComments(parsed.query, this.state.start_index)
			this.setState({value: parsed.query})
		}
	}

	handleChange(event){
		this.setState({value: event.target.value});
	}

	handleSubmit(event){
		let submission = this.state.value === "" ? this.suggestion : this.state.value
		let query = '?query=' + submission
		if (event) event.preventDefault();
		this.props.history.push({
		  pathname: '/',
			search: query,
			start_index: 0
		})
		this.getRelatedComments(submission, 0)
	}

	getRelatedComments(input_query) {
		if(input_query === "") {
			input_query = this.suggestion;
		}
		this.setState({loading: true})
		var arr = input_query.split(" ")
		var qParams = arr.map(key =>key).join('&');
		console.dir(qParams);
		console.log('running related comments fetch')
		console.log(this.state.start_index);
		axios.get('/search', {
				params: { start_index: this.state.start_index, query: qParams }
			})
		.then(response => {
			console.log(response)
			this.setState({
				data: response.data,
				hasSearched: true,
				loading: false,
				errored: false,
				numShowing: DEFAULT_NUM,
			})
		}).catch(error => {
			this.setState({ errored: true });
			console.error(error);
		});
	}

	showMore() {
		this.state.start_index += 10;
		this.getRelatedComments(this.state.value);
	}

	render() {
		let data = this.state.data.filter(comment => { return comment.body !== "[deleted]"})
    return (
    	<div>
    		<div>
    			<div className="header">
			      <form>
			      	<label>
			      		<p className = "title text-center">learnddit</p>
			      		<p className = "info text-center">see what's worked for redditors to learn</p>
			      		<p className = "info text-center">search for whatever you've wanted to learn and we'll tell you how <a href="https://reddit.com" target="_blank">reddit</a> users think you should learn it</p>
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
		      	{data.length ? <div className="tip">Hover over the IR score to see how comments are ranked!</div> : null}
			      {
			      	this.state.loading ? (<div className="loader"></div>) :
			      	(
			      		data.slice(this.props.history.start_index, this.state.numShowing).map((comment, i) => {
									console.log("rendering results")
			      		return <Result key={comment[0].id} comment={comment} style={i % 2 === 0 ? "white" : "whitesmoke"}/>})
		      		)
			      }
			      {
			      	data.length && !this.state.loading ?
			      		<button className="load-more" onClick={this.showMore}>Load more comments ({data.length - this.state.numShowing})</button> :
			      		null
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
