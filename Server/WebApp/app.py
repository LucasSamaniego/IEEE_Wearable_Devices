from flask import Flask, render_template, jsonify, request
import Info_material as item
import mqtt

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Dados fictícios para o dashboard
    data = {
        "sales_value": "$10,567",
        "growth": "10.57%",
        "customers": "345k",
        "customers_growth": "18.2%",
        "revenue": "$253,594",
        "revenue_change": "-4.6%",
        "dates": ["02 Feb", "03 Feb", "04 Feb", "05 Feb"],
        "values": [70, 60, 50, 40]
    }
    return render_template("index.html", data=data)

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/detalhes')
def detalhes():
    return render_template('detalhes.html')

@app.route('/contagem')
def contagem():
    return render_template('contagem.html')

@app.route('/movimentacao')
def movimentacao():
    return render_template('movimentacao.html')

# Rota para executar o script Python
@app.route('/run-python', methods=['POST'])
def run_python():
    try:

        # Obter o input enviado pelo front-end
        data = request.get_json()
        item_nome = data.get("input", "")

        objeto = item.Estocado(item_nome)
        objeto.detalhes()
        local = objeto.localizacao

        mqtt.navegar(local)
        
        # Retorna a localização do item
        return jsonify({
            'message': f'O item "{item_nome}" está localizado em: {local}'
        })
    
    except Exception as e:
        return jsonify({'message': f'Ocorreu um erro: {str(e)}'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
