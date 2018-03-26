// @flow
import { applyMiddleware, createStore, combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';

import array from './array';
import promise from './promise';
import reducers from '../reducers';
import thunk from 'redux-thunk';

let createClickerStore = applyMiddleware(thunk, promise, array)(createStore);

let configureStore = (onComplete: ?Object) => {
  let reducer = combineReducers({ ...reducers, routing: routerReducer });
  let store = createClickerStore(reducer, onComplete);
  return store;
};

export default configureStore;
