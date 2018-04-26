import React, { Component } from 'react';
import Truncate from 'react-truncate';

class Result extends Component {

  constructor(props){
    super(props);
    this.state = {
      expanded: false,
    }
    this.roundNearest = this.roundNearest.bind(this);
  }

  roundNearest(val) {
    let absVal = Math.abs(val);
    return Math.round(100*absVal)/100;
  }

  render() {
  	let comment = this.props.comment[0];
    let breakdown = this.props.comment[1];
    let irScore = this.roundNearest(breakdown[breakdown.length -1]);
    return (
    	<div className="comment" style={{backgroundColor: this.props.style}}>
    		<div className="comment-header">
    			<span className="author" ><a href={"http://reddit.com/u/" + comment.author} target="_blank">{comment.author}</a></span>
    			<span className="score">&nbsp; {comment.score} points &nbsp; IR score: {irScore}</span>
    		</div>
        {
          !this.state.expanded ?
          <Truncate lines={3} ellipsis={<div><div>...</div><button onClick={() => this.setState({expanded: true})}>read more</button></div>}>
                  {comment.body}
          </Truncate> :
          <div>
            <p>{comment.body}</p>
            <button onClick={() => this.setState({expanded: false})}>read less</button>
          </div>
        }
	    	<a className="permalink" href={comment.permalink} target="_blank">permalink</a>
        <a className="permalink" href={comment.link_id} target="_blank">&nbsp; thread</a>
	    	{/*<a className="permalink" href={"http://reddit.com/" + comment.subreddit} target="_blank"> {comment.subreddit}</a>*/}
    	</div>);
  }
}

export default Result;
