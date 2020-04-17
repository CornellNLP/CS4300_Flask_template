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
        
    }
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <input type="text" name="topicValue" onChange = {this.handleChange}></input>
                <input type="text" name="candidateValue" onChange = {this.handleChange}></input>
                <input type="text" name="debateValue" onChange = {this.handleChange}></input>
                <input type="submit" value="Add" ></input>
            </form>
        )
    }
}

export default InputForm;
