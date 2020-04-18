import React from 'react'
import './InputItems.css'

const types = ['topic', 'candidate', 'debate']
const colors = ['#29335C', '#DB2B39', '#F3A712']

class InputItems extends React.Component {
    constructor(props) {
        super(props); 
        this.removeItem = this.removeItem.bind(this)
    }
    removeItem(item) {
        this.props.removeItem(item)
    }
    render() {
        const { topics, candidates, debates } = this.props
        const topicItems = topics.map((item)=>
            <InputItem handleClick = {()=> this.removeItem(item)} itemName={item} type="topic"></InputItem>
        );
        const candidateItems = candidates.map((item)=>
            <InputItem handleClick = {()=> this.removeItem(item)} itemName={item} type="candidate"></InputItem>
        );
        const debateItems = debates.map((item)=>
            <InputItem handleClick = {()=> this.removeItem(item)} itemName={item} type="debate"></InputItem>
        );
        return (<div className="input-items">
            {topicItems}
            {candidateItems}
            {debateItems}
        </div>)
    }
}

/* going to return item of certain color based on type */
class InputItem extends React.Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this)
    }
    handleClick() {
        this.props.handleClick();
    }
    render(){
        const { itemName, type } = this.props
        
        const style = {
            backgroundColor: colors[types.indexOf(type)]
        }

        return (
            <div style={style} className = "input-item_div_wrapper">
                <div className="input-item_name">{itemName}</div>
                <div className="input-item_delete" onClick={this.handleClick}>X</div>
            </div>
        )
    } 
}

export default InputItems;