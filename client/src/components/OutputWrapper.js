import React from 'react';
import DebateItem from './DebateItem';
import './OutputWrapper.css'

class OutputWrapper extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        const debateItems = this.props.outputs && this.props.outputs.map((output) => 
            <DebateItem
                title = {output.title}
                date = {output.date}
                description = {output.description}
                results = {output.results}
            >
            </DebateItem>
        )
        return (
            <div className="output-wrapper">
                {debateItems}
            </div>
        )
    }
}

export default OutputWrapper