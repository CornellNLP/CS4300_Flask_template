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

var _Slide = _interopRequireDefault(require("./Slide"));

/**
 * @ignore - internal component.
 */
var StrictModeSlide = React.forwardRef(function StrictModeSlide(props, forwardedRef) {
  var domRef = React.useRef(null);
  var ref = (0, _utils.useForkRef)(domRef, forwardedRef);
  return /*#__PURE__*/React.createElement(_Slide.default, (0, _extends2.default)({}, props, {
    findDOMNode: function findDOMNode() {
      return domRef.current;
    },
    ref: ref,
    TransitionComponent: _reactTransitionGroup.Transition
  }));
});
var _default = StrictModeSlide;
exports.default = _default;