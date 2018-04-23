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
    			<span className="author" ><a href={"http://reddit.com/u/" + comment.author} target="_blank">{comment.author}</a></span>
    			<span className="score">&nbsp; {comment.score} points</span>
    		</div>
	    	<p>{comment.body}</p>
	    	<a className="permalink" href={comment.permalink} target="_blank">permalink</a>
        <a className="permalink" href={comment.link_id} target="_blank">&nbsp; thread</a>
	    	{/*<a className="permalink" href={"http://reddit.com/" + comment.subreddit} target="_blank"> {comment.subreddit}</a>*/}
    	</div>);
  }
}

export default Result;
