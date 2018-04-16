import React, { Component } from 'react';

class Result extends Component {

  constructor(props){
    super(props);
  }

  render() {
    return (<div><p>{this.props.body}</p></div>);
  }
}