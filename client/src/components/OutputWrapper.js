import React from 'react';
import DebateItem from './DebateItem';
import Anime from 'react-anime';
import './OutputWrapper.css'

class OutputWrapper extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        const debateItems = this.props.outputs && this.props.outputs.map((output, i) => 
            <DebateItem
                title = {output.title}
                date = {output.date}
                description = {output.description}
                results = {output.results}
                key={i}
            >
            </DebateItem>
        )

        let animeProps = {
            opacity: [0,1],
            translateY: [-64,0], 
            delay: (el,i) => i*200
        }
        return (
            <div className="output-wrapper">
                <Anime {...animeProps}>
                {debateItems}
                </Anime>
            </div>
        )
    }
}

export default OutputWrapper