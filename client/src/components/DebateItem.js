import React from 'react'; 
import './DebateItem.css'
import ResultItem from './ResultItem'

class DebateItem extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        const { title, date, description, results } = this.props;
        const resultItems = results.map((result) =>
            <ResultItem 
                video={result.video}
                quotes={result.quotes}
            ></ResultItem>
        )
        return (
            <div className = "debate-item-wrapper">
                <DebateDescription
                    title={title}
                    date={date}
                    description={description}
                >
                </DebateDescription>
                {resultItems}
            </div>
        )
    }
}

function DebateDescription(props) {
    return (
        <div>
            <div className="debate-title">{props.title}</div>
            <div className="debate-date">{props.date}</div>
            <div className="debate-description">{props.description}</div>
        </div>
    )
}

export default DebateItem;