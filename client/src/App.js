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
      <h1>Shortened Debates.</h1>
      <InputWrapper onInputChange={this.sendInputInformation} onClear={this.onClear}/>
      <OutputWrapper outputs={this.state.output}></OutputWrapper>
    </div>
  );
}
}

export default App;

const dummyData = [
  {
    title: 'DEBATE 1', 
    date: 'some date', 
    description: 'some description',
    results: [
      {
        video: 'some url', 
        quotes: [
          {
            speaker: '', 
            candidate: false, 
            question: true, 
            time: '', 
            text: ''
          }, 
          {
            speaker: '', 
            candidate: true, 
            question: false, 
            time: '', 
            text: '' 
          }
        ]
      }, 
      {
        video: 'some url', 
        quotes: [
          {
            speaker: '', 
            candidate: false, 
            question: true, 
            time: '', 
            text: ''
          }, 
          {
            speaker: '', 
            candidate: true, 
            question: false, 
            time: '', 
            text: '' 
          }
        ]
      }
    ]
  }, 
  {
    title: 'DEBATE 2', 
    date: 'some date', 
    description: 'some description',
    results: [
      {
        video: 'some url', 
        quotes: [
          {
            speaker: '', 
            candidate: false, 
            question: true, 
            time: '', 
            text: ''
          }, 
          {
            speaker: '', 
            candidate: true, 
            question: false, 
            time: '', 
            text: '' 
          }
        ]
      }, 
      {
        video: 'some url', 
        quotes: [
          {
            speaker: '', 
            candidate: false, 
            question: true, 
            time: '', 
            text: ''
          }, 
          {
            speaker: '', 
            candidate: true, 
            question: false, 
            time: '', 
            text: '' 
          }
        ]
      }
    ]
  }
]