import React from 'react';
import axios from 'axios';

// css files 
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/main.css';
import './css/App.css';

// images, lists
import logo from './images/operator.png';
import scores from './images/scores';

// components
import Form from './components/Form'
import JokeResults from './components/JokeResults';
import AutoCompleteText from './components/AutoCompleteText';

// import { Button, Checkbox, Form } from 'semantic-ui-react'
import { Row, Col, Container } from 'react-bootstrap'
import {CircularProgress} from '@material-ui/core'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      isLoaded: false,
      jokes: [],

      category: '',
      score: '',
      search: ''    }
  }

  componentDidMount() {
    const URLParams = new URLSearchParams(this.props.location.search)

    console.log(URLParams)
    const category_param = URLParams.getAll("category")
    const score_param = URLParams.get("score")
    const search_param = URLParams.get("search")

    axios({
        method: 'GET',
        url: `http://localhost:5000/api/search`,
        params: URLParams
      })
      .then((response) => {
        this.setState({
          isLoaded:true,
          jokes: response.data.jokes,
          
          category: category_param,
          score: score_param,
          search : search_param
        })
      })
      .catch(err =>
        console.log(err)
      );
  }

  render() {
    if (this.state.isLoaded) return (
      <Container>
        <Row className="justify-content-md-center">
          <Col>
            <header className="App-header">
              <h1>HahaFactory</h1>
              <img src={logo} className="App-logo" alt="logo" />
            </header>

          <Form score = {this.state.score} categories = {this.state.category} search = {this.state.search} />

          </Col>
        </Row>
        <Row>
          <Col className="jokes-col">
            <JokeResults jokes={this.state.jokes} />
          </Col>
        </Row>
      </Container >
      )
      else return (
       <p> loading ...</p>
      )
  }
}

export default App;
