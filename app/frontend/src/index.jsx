import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom'

import './css/index.css';
import Home from './components/Home';
import $ from 'jquery'

// place a Header component on the line above Switch to get a universal header
const Root = () => {
  <BrowserRouter>
    <Switch>
      <Route exact path='/' component={Home}/>
    </Switch>
  </BrowserRouter>
}

ReactDOM.render(<Home />, document.getElementById('root'));
