"use strict";

var _interopRequireDefault = require("@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = createMuiStrictModeTheme;

var _utils = require("@material-ui/utils");

var _createMuiTheme = _interopRequireDefault(require("./createMuiTheme"));

var _Collapse = require("../Collapse");

var _Fade = require("../Fade");

var _Grow = require("../Grow");

var _Slide = require("../Slide");

var _Zoom = require("../Zoom");

function createMuiStrictModeTheme(options) {
  return (0, _createMuiTheme.default)((0, _utils.deepmerge)({
    props: {
      // Collapse
      MuiExpansionPanel: {
        TransitionComponent: _Collapse.unstable_StrictModeCollapse
      },
      MuiStepContent: {
        TransitionComponent: _Collapse.unstable_StrictModeCollapse
      },
      // Fade
      MuiBackdrop: {
        TransitionComponent: _Fade.unstable_StrictModeFade
      },
      MuiDialog: {
        TransitionComponent: _Fade.unstable_StrictModeFade
      },
      // Grow
      MuiPopover: {
        TransitionComponent: _Grow.unstable_StrictModeGrow
      },
      MuiSnackbar: {
        TransitionComponent: _Grow.unstable_StrictModeGrow
      },
      MuiTooltip: {
        TransitionComponent: _Grow.unstable_StrictModeGrow
      },
      // Slide
      MuiDrawer: {
        TransitionComponent: _Slide.unstable_StrictModeSlide
      },
      // Zoom
      MuiSpeedDial: {
        TransitionComponent: _Zoom.unstable_StrictModeZoom
      }
    }
  }, options));
}