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
            <div>
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
            <h2>{props.title}</h2>
            <h3>{props.date}</h3>
            <p>{props.description}</p>
        </div>
    )
}

export default DebateItem;