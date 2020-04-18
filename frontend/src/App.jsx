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


function App() {
  return (

    <Container>
      <Row className="justify-content-md-center">
        <Col>
          <header className="App-header">
            <h1>HahaFactory</h1>
            <img src={logo} className="App-logo" alt="logo" />
          </header>
          <Form className="global-search">

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
    </Container >


  );
}

export default App;
