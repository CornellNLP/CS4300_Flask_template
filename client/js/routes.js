// @flow
import React from 'react';
import { Route, IndexRoute } from 'react-router';

import App from './components/App';
import Home from './components/Home';

const routes: React.Element<any> = (
  <Route path='/' component={App}>
    <IndexRoute component={Home} />
  </Route>
);

export default routes;
