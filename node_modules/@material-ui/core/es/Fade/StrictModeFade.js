import _extends from "@babel/runtime/helpers/esm/extends";
import * as React from 'react';
import { Transition } from '@material-ui/react-transition-group';
import { useForkRef } from '../utils';
import Fade from './Fade';
/**
 * @ignore - internal component.
 */

const StrictModeFade = React.forwardRef(function StrictModeFade(props, forwardedRef) {
  const domRef = React.useRef(null);
  const ref = useForkRef(domRef, forwardedRef);
  return /*#__PURE__*/React.createElement(Fade, _extends({}, props, {
    findDOMNode: () => domRef.current,
    ref: ref,
    TransitionComponent: Transition
  }));
});
export default StrictModeFade;