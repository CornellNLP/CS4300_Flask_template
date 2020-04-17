import React from 'react';
import './App.css';
import InputWrapper from './components/InputWrapper';
import OutputWrapper from './components/OutputWrapper';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      input: {},
      output: []
    }
    this.setSocketListeners = this.setSocketListeners.bind(this)
    this.sendInputInformation = this.sendInputInformation.bind(this)
    this.onClear = this.onClear.bind(this)
  }
  componentDidMount() {
    this.setSocketListeners()
  }
  setSocketListeners() {
    socket.on('output_sent', (data)=> {
      this.setState({
        output: data
      })
    }) 
  }
  sendInputInformation(newInput) {
    this.setState({
      input: newInput
    }, ()=>{
      socket.emit('input_change',{results: this.state.input})
    })
  }
  onClear() {
    this.setState({
      output: []
    })
  }
  render(){
    return (
    <div className="App">
      <h1 className="app-title">Shortened Debates.</h1>
      <p className="app-description">watch the important moments on the issues you are care about.</p>
      <InputWrapper onInputChange={this.sendInputInformation} onClear={this.onClear}/>
      <OutputWrapper outputs={this.state.output}></OutputWrapper>
    </div>
  );
}
}

export default App;
