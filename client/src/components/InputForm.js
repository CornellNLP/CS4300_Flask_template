import React from 'react';
import './InputForm.css';

class InputForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            topicValue: '', 
            candidateValue: '', 
            debateValue: ''
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }
    handleChange(event) {
        const name = event.target.name
        this.setState({
            [name]: event.target.value
        })
    }
    handleSubmit(event) {
        event.preventDefault();
        const state = this.state
        this.props.onAddChange(state.topicValue, state.candidateValue, state.debateValue);
        this.setState({
            topicValue: '', 
            candidateValue: '', 
            debateValue: ''
        })
        
    }
    render() {
        return (
            <div>
                <form>
                    <input value = {this.state.topicValue} placeholder="topic: climate change" className="input-topic" type="text" name="topicValue" onChange = {this.handleChange}></input>
                    <input value = {this.state.candidateValue} placeholder="candidate: Bernie Sanders" className="input-candidate" type="text" name="candidateValue" onChange = {this.handleChange}></input>
                    <input value = {this.state.debateValue} placeholder="debate: South Carolina Democratic Primary" className="input-debate" type="text" name="debateValue" onChange = {this.handleChange}></input>
                    <input className="button-add" type="button" onClick={this.handleSubmit} value="Add" ></input>
                </form>
                <div className="input-message">Separate by commas for multiple topics, candidates, or debates</div>
            </div>
        )
    }
}

export default InputForm;
