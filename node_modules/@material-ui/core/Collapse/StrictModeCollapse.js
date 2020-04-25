"use strict";

var _interopRequireWildcard = require("@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _extends2 = _interopRequireDefault(require("@babel/runtime/helpers/extends"));

var React = _interopRequireWildcard(require("react"));

var _reactTransitionGroup = require("@material-ui/react-transition-group");

var _utils = require("../utils");

var _Collapse = _interopRequireDefault(require("./Collapse"));

/**
 * @ignore - internal component.
 */
var StrictModeCollapse = React.forwardRef(function StrictModeCollapse(props, forwardedRef) {
  var domRef = React.useRef(null);
  var ref = (0, _utils.useForkRef)(domRef, forwardedRef);
  return /*#__PURE__*/React.createElement(_Collapse.default, (0, _extends2.default)({}, props, {
    findDOMNode: function findDOMNode() {
      return domRef.current;
    },
    ref: ref,
    TransitionComponent: _reactTransitionGroup.Transition
  }));
});
var _default = StrictModeCollapse;
exports.default = _default;