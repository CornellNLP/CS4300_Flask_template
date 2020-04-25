import _extends from "@babel/runtime/helpers/esm/extends";
import * as React from 'react';
import { Transition } from '@material-ui/react-transition-group';
import { useForkRef } from '../utils';
import Collapse from './Collapse';
/**
 * @ignore - internal component.
 */

var StrictModeCollapse = React.forwardRef(function StrictModeCollapse(props, forwardedRef) {
  var domRef = React.useRef(null);
  var ref = useForkRef(domRef, forwardedRef);
  return /*#__PURE__*/React.createElement(Collapse, _extends({}, props, {
    findDOMNode: function findDOMNode() {
      return domRef.current;
    },
    ref: ref,
    TransitionComponent: Transition
  }));
});
export default StrictModeCollapse;