// @flow
module.exports = (store: Object) => (next: Function) => (action: Function) =>
  Array.isArray(action)
    ? action.map(next)
    : next(action);
