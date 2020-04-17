import React from 'react'; 
import './ResultItem.css'

class ResultItem extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        const {video, quotes} = this.props
        const quoteItems = quotes.map(quote => 
            <Quote
                speaker = {quote.speaker}
                candidate = {quote.candidate}
                question = {quote.candidate}
                time = {quote.time}
                text = {quote.text}
            ></Quote>
        )
        return (
            <div>
                <video width="250">
                    {video}
                </video>
                {quoteItems}
            </div>
        )
    }
}

function Quote(props) {
    const {speaker, candidate, question, time, text} = props  
    return(
        <div>
            <h5>{speaker}</h5>
            <h6>{time}</h6>
            <p>{text}</p>
        </div>
    )
}

export default ResultItem;