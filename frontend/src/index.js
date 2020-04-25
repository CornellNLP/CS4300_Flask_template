import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

import { BrowserRouter, Route, Switch } from 'react-router-dom';
import SampleFetch from './components/SampleFetch';


ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route path="/" component={App} />
      {/* <Route path="/sample" component={SampleFetch} /> */}
    </Switch>
  </BrowserRouter>, document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
