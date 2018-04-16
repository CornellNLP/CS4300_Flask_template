import React, { Component } from 'react';

class Result extends Component {

  constructor(props){
    super(props);
  }

  render() {
  	let comment = this.props.comment;
    return (
    	<div className="comment" style={{backgroundColor: this.props.style}}>
    		<div className="comment-header">
    			<span className="author" >{comment.author}</span>
    			<span className="score"> {comment.score} points</span>
    			<span className="votes"> {comment.ups} upvotes</span>
    			<span className="votes"> {comment.downs} downvotes</span>
    		</div>
	    	<p>{comment.body}</p>
	    	<a className="permalink" href={"http://reddit.com/" + comment.permalink} target="_blank">permalink</a>
	    	<a className="permalink" href={"http://reddit.com/" + comment.subreddit} target="_blank"> {comment.subreddit}</a>
    	</div>);
  }
}

export default Result;
