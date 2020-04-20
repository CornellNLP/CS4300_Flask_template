from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder


@socketio.on('input_change')
def on_input_change(data):
  print(data)
  socketio.emit('output_sent', debates)


