from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder


with open('fake_data.json', 'r') as f:
  fake_data = json.load(f)

@socketio.on('input_change')
def on_input_change(data):
  print(data)
  socketio.emit('output_sent', fake_data)


