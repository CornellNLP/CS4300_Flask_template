import React from 'react'; 
import './DebateItem.css'
import ResultItem from './ResultItem'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {  faChevronRight } from '@fortawesome/free-solid-svg-icons'

class DebateItem extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            openItem: false
        }
        this.handleClick = this.handleClick.bind(this)
    }
    handleClick() {
        this.setState({
            openItem: !this.state.openItem
        })
    }
    render() {
        const { title, date, description, results } = this.props;
        const resultItems = results.map((result) =>
            <ResultItem 
                video={result.video}
                quotes={result.quotes}
            ></ResultItem>
        )
        const degrees = this.state.openItem ? 90 : 0
        return (
            <div className = "debate-item-wrapper">
                <div>
                    <div className="debate-title-wrapper"><div className="debate-title" onClick={this.handleClick}>{title}</div><FontAwesomeIcon rotation={degrees} icon={faChevronRight} /></div>
                    <div className="debate-date">{date}</div>
                    {this.state.openItem && <div className="debate-description">{description}</div>}
                </div>
                {this.state.openItem && resultItems}
            </div>
        )
    }
}


export default DebateItem;