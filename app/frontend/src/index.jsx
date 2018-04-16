import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom'

import './css/index.css';
import Home from './components/Home';
import Result from './components/Result';

// place a Header component on the line above Switch to get a universal header
const Root = () => {
  <BrowserRouter>
      <Route exact path='/' component={Home}/>
  </BrowserRouter>
}

ReactDOM.render(<Home />, document.getElementById('root'));
