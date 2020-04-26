import React from 'react';
import axios from 'axios';
import logo from './images/operator.png';
import 'bootstrap/dist/css/bootstrap.min.css';

import './css/main.css';
import './css/App.css';
import AutoCompleteText from './components/AutoCompleteText';
import categories from './images/categories';
import scores from './images/scores'

import Form from 'react-bootstrap/Form'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Container from 'react-bootstrap/Container'
import Button from 'react-bootstrap/Button'

import JokeResults from './components/JokeResults';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      isLoaded: false,
      jokes: [],
    }
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  
  handleSubmit(event) {
    console.log("submit")
    // event.preventDefault();
    const data = new FormData(event.target);

    fetch('http://localhost:5000/api/jokes', {
      method: 'GET',
      // body: data,
    })
      .then(res => res.json())
      .then(
        (data) => {

          this.setState({
            isLoaded: true,
            jokes: data.jokes
          });

        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
    // .then(console.log(this.jokes))
  }

  render() {
    console.log("hi")
    console.log(this.state.cat_options)
    const categoryList = this.state.cat_options.map((cat) =>
      <option value={cat}>{cat}</option>
    );

    const scoreList = scores.map((score) =>
      <option value={score}>{score}</option>
    );

        return (
      <Container>
        <Row className="justify-content-md-center">
          <Col>
            <header className="App-header">
              <h1>HahaFactory</h1>
              <img src={logo} className="App-logo" alt="logo" />
            </header>

            
            <Form className="global-search" onSubmit={this.handleSubmit}>

              <Form.Group controlId="Key Words" className="formGroupCenter">
                <Form.Control
                  type="text"
                  name="name"
                  // value={this.state.newRequest.contactinfo.name}
                  // onChange={this.handleInput_contact}
                  placeholder="Enter Key Words..."
                  required
                />
              </Form.Group>

              {/* <Form.Group controlId="category" className="formGroupCenter">
                <Form.Label>Category:</Form.Label>
                <Form.Control as="select">
                  <option>Enter Category...</option>
                  <option>1</option>
                  <option>2</option>
                </Form.Control>
              </Form.Group> */}

              <Form.Group controlId="category_autocomplete" className="formGroupCenter">
                <Form.Label className="category_label">Category:</Form.Label> 
                <div className="App">
                  <div className="App-Component">
                    <div className="App-Component">
                      <AutoCompleteText items={categories} />
                    </div>
                  </div>
                </div>
              </Form.Group>


              <Form.Group controlId="min_score" className="formGroupCenter">
                <Form.Label>Minimum Score:</Form.Label>
                {['radio'].map((type) => (
                  <div key={`inline-${type}`} className="score_options">
                    <Form.Check inline label="1" type={type} id={`inline-${type}-1`} />
                    <Form.Check inline label="2" type={type} id={`inline-${type}-2`} />
                    <Form.Check inline label="3" type={type} id={`inline-${type}-3`} />
                    <Form.Check inline label="4" type={type} id={`inline-${type}-4`} />
                    <Form.Check inline label="5" type={type} id={`inline-${type}-5`} />
                  </div>
                ))}
              </Form.Group>

              <Form.Group controlId="maturity_rating" className="formGroupCenter">
                <Form.Label>Maturity Rating:</Form.Label>
                <Form.Control as="select">
                  <option>Enter Maturity Rating...</option>
                  <option>PG</option>
                  <option>PG-13</option>
                  <option>R</option>
                </Form.Control>
              </Form.Group>

              <Button type="submit" className="btn btn-info">Go!</Button>
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
  }
}

export default App;
