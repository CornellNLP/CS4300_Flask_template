import React from 'react';
import InputForm from './InputForm';
import InputItems from './InputItems';

class InputWrapper extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            topics: [],
            candidates: [],
            debates: [], 
            errorOn: false
        }
        this.onAddChange = this.onAddChange.bind(this);
        this.removeItem = this.removeItem.bind(this);
    }
    removeItem(item) {
        this.setState({
            topics: this.state.topics.filter(el => el !== item),
            candidates: this.state.candidates.filter(el => el !== item),
            debates: this.state.debates.filter(el => el !== item)
        }, () => {
            if (this.state.topics.length) {
                this.setState({
                    errorOn: false
                })
                this.props.onInputChange(
                    { 
                        topics: this.state.topics, 
                        candidates: this.state.candidates, 
                        debates: this.state.debates
                    }
                )
            }
            else {
                this.setState({
                    errorOn: true
                })
                this.props.onClear()
            }
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
        }, () => {
            if (this.state.topics.length) {
                this.setState({
                    errorOn: false
                })
                this.props.onInputChange(
                    { 
                        topics: this.state.topics, 
                        candidates: this.state.candidates, 
                        debates: this.state.debates
                    }
                )
            }
            else {
                this.setState({
                    errorOn: true
                })
                this.props.onClear()
            }
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
            <ErrorMessage errorOn={this.state.errorOn}></ErrorMessage>
        </div>
        )
        
    }
}

function ErrorMessage(props) {
    if (props.errorOn) {
        return (
        <div>
            Please insert atleast 1 topic!
        </div>
    )
    }
    return null; 
}

export default InputWrapper;