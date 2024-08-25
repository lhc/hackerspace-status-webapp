from flask import Flask, render_template, redirect, url_for, jsonify
from multiprocessing import Process
from lstatus.database import DatabaseHandler
from lstatus.edge import EdgeController

app = Flask(__name__)
db_handler = DatabaseHandler()
edge_controller = EdgeController()

@app.route('/')
def index():
    logs = db_handler.get_logs()
    current_status = db_handler.get_last_event()
    if not current_status:
        current_status = 'LHC Fechado'
    return render_template('index.html', logs=logs, current_status=current_status)

@app.route('/lhc_aberto')
def lhc_aberto():
    db_handler.log_event('LHC Aberto')
    return redirect(url_for('index'))

@app.route('/lhc_fechado')
def lhc_fechado():
    db_handler.log_event('LHC Fechado')
    return redirect(url_for('index'))

@app.route('/api/status/lhc')
def api_status_lhc():
    log = db_handler.get_logs(1)
    if log:
        response = {
            'id': log[0][0],
            'event': log[0][1],
            'timestamp': log[0][2]
        }
    else:
        response = {
            'message': 'No logs found'
        }
    return jsonify(response)

if __name__ == '__main__':
    # Cria um processo separado para monitorar o botão
    p = Process(target=edge_controller.monitor_button)
    p.start()
    
    # Inicia o servidor Flask
    app.run(host="0.0.0.0", debug=True)
    
    # Espera o processo do botão terminar (embora isso nunca deva acontecer)
    p.join()
