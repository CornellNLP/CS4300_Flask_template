import React from 'react';
import logo from './operator.png';
import 'bootstrap/dist/css/bootstrap.min.css';

import './main.css';
import './App.css';

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
      jokes: []
    }
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);

    fetch('http://0.0.0.0:5000/jokes/api', {
      mode: 'no-cors',
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
  }

  render() {
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
                  placeholder="Enter key words..."
                  required
                />
              </Form.Group>

              <Button type="submit" class="btn btn-info">Go!</Button>
            </Form>

          </Col>
        </Row>
        <Row>
          <Col>
            <JokeResults jokes={this.state.jokes} />
          </Col>
        </Row>
      </Container >


    );
  }

}

export default App;
