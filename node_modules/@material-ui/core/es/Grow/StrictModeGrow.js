import _extends from "@babel/runtime/helpers/esm/extends";
import * as React from 'react';
import { Transition } from '@material-ui/react-transition-group';
import { useForkRef } from '../utils';
import Grow from './Grow';
/**
 * @ignore - internal component.
 */

const StrictModeGrow = React.forwardRef(function StrictModeGrow(props, forwardedRef) {
  const domRef = React.useRef(null);
  const ref = useForkRef(domRef, forwardedRef);
  return /*#__PURE__*/React.createElement(Grow, _extends({}, props, {
    findDOMNode: () => domRef.current,
    ref: ref,
    TransitionComponent: Transition
  }));
});
export default StrictModeGrow;