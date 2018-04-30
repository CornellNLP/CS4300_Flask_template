import React, { Component } from 'react';
import Truncate from 'react-truncate';

class Result extends Component {

  constructor(props){
    super(props);
    this.state = {
      expanded: false,
      showBreakdown: false,
      showExplicit: false
    }
    this.showScore = this.showScore.bind(this);
    this.roundNearest = this.roundNearest.bind(this);
  }

  onClick(e) {
    e.preventDefault();
    this.setState({ showExplicit: true })
  }

  roundNearest(val) {
    let absVal = Math.abs(val);
    return Math.round(100*absVal)/100;
  }

  showScore() {
    let breakdown = this.props.comment[1];
    let showBreakdown = this.state.showBreakdown;
    this.setState({ showBreakdown: !showBreakdown })
  }

  checkExplicit(comment) {
    let explicitWords = ["fuck", "shit", "bitch", "cunt", "bastard"];
    for (var i = 0; i < explicitWords.length; i++) {
      if (comment.indexOf(explicitWords[i]) != -1) {
        return true;
      }
    }
    return false;
  }

  render() {
    let breakdownLabel = ["Cos-sim score:", " x # of noun terms:", ' x √(comment score):']
    let colors = ["blue", "green", "red"]

  	let comment = this.props.comment[0];
    let breakdown = this.props.comment[1];
    let irScore = this.roundNearest(breakdown[breakdown.length -1]);
    let visibilityState = this.state.showBreakdown ? "visible" : "hidden";
    let explicit = this.checkExplicit(comment.body)
    let expVisibilityState = (explicit && !this.state.showExplicit) ? "visible" : "hidden";
    return (
    	<div className="comment" style={{backgroundColor: this.props.style}}>
    		<div className="comment-header">
    			<span className="author"><a href={"http://reddit.com/u/" + comment.author} target="_blank">{comment.author}</a></span>
    			<span className="score" onMouseEnter={this.showScore} onMouseLeave={this.showScore}>&nbsp; {comment.score} points &nbsp; IR score: {irScore}</span>
          <span className="score" style={{visibility: visibilityState}}>
            &nbsp;|{breakdownLabel.map((label, i) => <span>{label}<span style={{color: colors[i]}}> {this.roundNearest(breakdown[i])}</span></span>)}
          </span>
    		</div>
        <div className={(explicit && !this.state.showExplicit) ? 'explicit' : ''} onClick={this.onClick.bind(this)}>
          <p style={{visibility: expVisibilityState}}>Warning: this content contains expletives. Click to reveal.</p>
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
        </div>
	    	<a className="permalink" href={comment.permalink} target="_blank">permalink</a>
        <a className="permalink" href={comment.link_id} target="_blank">&nbsp; thread</a>
	    	{/*<a className="permalink" href={"http://reddit.com/" + comment.subreddit} target="_blank"> {comment.subreddit}</a>*/}
    	</div>);
  }
}

export default Result;
