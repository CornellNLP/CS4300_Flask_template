import _extends from "@babel/runtime/helpers/esm/extends";
import * as React from 'react';
import { Transition } from '@material-ui/react-transition-group';
import { useForkRef } from '../utils';
import Grow from './Grow';
/**
 * @ignore - internal component.
 */

var StrictModeGrow = React.forwardRef(function StrictModeGrow(props, forwardedRef) {
  var domRef = React.useRef(null);
  var ref = useForkRef(domRef, forwardedRef);
  return /*#__PURE__*/React.createElement(Grow, _extends({}, props, {
    findDOMNode: function findDOMNode() {
      return domRef.current;
    },
    ref: ref,
    TransitionComponent: Transition
  }));
});
export default StrictModeGrow;