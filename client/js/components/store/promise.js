// @flow
let warn = (error) => {
  console.warn(error.message || error);
  throw error; // To let the caller handle the rejection
};

module.exports = (store: Object) => (next: Function) => (action: Function) =>
  typeof action.then === 'function'
    ? Promise.resolve(action).then(next, warn)
    : next(action);
