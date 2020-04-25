import React from 'react';
import axios from 'axios';
import logo from './images/operator.png';
import 'bootstrap/dist/css/bootstrap.min.css';

import './css/main.css';
import './css/App.css';
import AutoCompleteText from './components/AutoCompleteText';
import scores from './images/scores';

import { Button, Checkbox, Form } from 'semantic-ui-react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'

import JokeResults from './components/JokeResults';
import {CircularProgress} from '@material-ui/core'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      isLoaded: false,
      jokes: [],
      cat_options: [],

      category: '',
      score: '',
      search: ''    }
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    const URLParams = new URLSearchParams(this.props.location.search)

    axios.all([
      axios({
        method: 'GET',
        url: `http://localhost:5000/api/search`,
        params: URLParams
      }),
      axios({
        method: 'GET',
        url: `http://localhost:5000/api/cat-options`
      })
    ])
      .then(axios.spread((response1, response2) => {
        this.setState({
          isLoaded:true,
          jokes: response1.data.jokes,
          cat_options: response2.data.categories
        })
      }))
      .catch(err =>
        console.log(err)
      );
  }

  handleChange = (e, { name, value }) => this.setState({ [name]: value })
  
  handleSubmit(event) {
    event.preventDefault();

    const { search, category, score} = this.state
    const data = new FormData(event.target);
    const params = new URLSearchParams()
    console.log(this.state)
    params.append("search", search)
    
    category.forEach(cat => {
      params.append("category", cat);
    })
   
    params.append("score", score)
    this.props.history.push({
      //something but too tired rn 
    })

    axios({
      method: 'GET',
      url: `http://localhost:5000/api/search`,
      params: params
    })
    .then (response => {
      this.setState({
        jokes: response.data.jokes
      })
    })
    .catch(err => 
      console.log(err));
    
  }

  render() {
    const categoryList = this.state.cat_options.map((cat) =>
        ({key: cat,
        text: cat,
        value: cat})        
    );

    const scoreList = scores.map((score) =>
      ({key: score, 
      text: score, 
      value: score})
    );

    return (
      <Container>
        <Row className="justify-content-md-center">
          <Col>
            <header className="App-header">
              <h1>HahaFactory</h1>
              <img src={logo} className="App-logo" alt="logo" />
            </header>

            <Form onSubmit={this.handleSubmit}>
              <Form.Input
                placeholder="Search"
                name="search"
                label = "Keywords" 
                type = "text"
                onChange={this.handleChange}/>

              <Form.Dropdown
                placeholder = "Select Categories"
                name = "category"
                label = "Categories"
                multiple
                search
                selection
                options = {categoryList}
                onChange={this.handleChange}
              />

              <Form.Dropdown
                placeholder="Select Minimum Score"
                name="score"
                label="Minimum Score"
                selection
                options={scoreList}
                onChange={this.handleChange}
              />

              <button class="ui button" type="submit">Go</button>
            </Form>

          </Col>
        </Row>
        <Row>
          <Col className="jokes-col">
            <JokeResults jokes={this.state.jokes} />
          </Col>
        </Row>
      </Container >


      )
    //   {
    //   return <div style={{ display: 'flex', position: 'absolute', left: '50%', top: '50%' }}>
    //     <CircularProgress disableShrink />
    //   </div>
    // }
  }

}

export default App;
