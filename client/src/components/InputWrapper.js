import React from 'react';
import InputForm from './InputForm';
import InputItems from './InputItems';

class InputWrapper extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            topics: [],
            candidates: [],
            debates: []
        }
        this.onAddChange = this.onAddChange.bind(this);
        this.removeItem = this.removeItem.bind(this);
    }
    removeItem(item) {
        this.setState({
            topics: this.state.topics.filter(el => el !== item),
            candidates: this.state.candidates.filter(el => el !== item),
            debates: this.state.debates.filter(el => el !== item)
        })
        
    }
    onAddChange(topicValue, candidateValue, debateValue) {
        const {topics, candidates, debates} = this.state

        const newTopics = topicValue === '' ? '' : topicValue.split(',')
        const newCandidates = candidateValue === '' ? '' :candidateValue.split(',')
        const newDebates = debateValue === '' ? '' : debateValue.split(',')

        this.setState({
            topics: [...new Set([...topics, ...newTopics])],
            candidates: [...new Set([...candidates, ...newCandidates])], 
            debates: [...new Set([...debates, ...newDebates])]
        });
    }
    render(){
        return(
            <div>
            <InputForm onAddChange={this.onAddChange}></InputForm>
            <InputItems 
                topics={this.state.topics} 
                candidates={this.state.candidates}
                debates={this.state.debates}
                removeItem={this.removeItem}
                ></InputItems>
        </div>
        )
        
    }
}

export default InputWrapper;