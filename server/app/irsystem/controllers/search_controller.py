from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import search


@socketio.on('input_change')
def on_input_change(data):
    # data format: {'results': {'topics': [], 'candidates': [], 'debates': []}}

    # TODO: actually pick the relevant debates
    debate_name = data['results']['debates'][0]

    results = search(data['results']['topics'], data['results']['candidates'], debate_name)
    socketio.emit('output_sent', results)
