// @flow
import { render } from 'react-dom';
import { Router, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import { Provider } from 'react-redux';
import React from 'react';

import configureStore from './components/store/configureStore';
import routes from './routes';

const store = configureStore();
const history = syncHistoryWithStore(browserHistory, store);

const router: React.Element<any> = (
  <Provider store={store}>
    <Router history={history} routes={routes} />
  </Provider>
);

render(router, document.getElementById('root'));
