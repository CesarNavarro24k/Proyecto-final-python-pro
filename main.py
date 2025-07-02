# Importar
from flask import Flask, render_template, request
from password import token
import yagmail

app = Flask(__name__)

def result_calculate(size, lights, device):
    # Variables que permiten calcular el consumo energético de los aparatos
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5   
    return size * home_coef + lights * light_coef + device * devices_coef 

# La primera página
@app.route('/')
def index():
    return render_template('index.html')

# Segunda página
@app.route('/mouse')
def mouse():
    return render_template('mouse.html')

# La tercera página - Corregida para recibir parámetros de la URL
@app.route('/teclados')
def teclados():
    size = request.args.get('size', 0)
    lights = request.args.get('lights', 0)
    return render_template('electronics.html',                           
                          size=size, 
                          lights=lights)

# Cálculo - Corregida para recibir parámetros de la URL
@app.route('/monitores')
def monitores():
    size = request.args.get('size', 0)
    lights = request.args.get('lights', 0)
    device = request.args.get('device', 0)
    return render_template('end.html', 
                          result=result_calculate(int(size),
                                                int(lights), 
                                                int(device)))

# El formulario
@app.route('/form')
def form():
    return render_template('form.html')

# Resultados del formulario
@app.route('/submit', methods=['POST'])
def submit_form():
    # Declarar variables para la recogida de datos
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']

    return render_template('form_result.html', 
                          name=name, 
                          email=email,
                          address=address, 
                          date=date)

# Nueva ruta para enviar correos
@app.route('/send_email')
def send_email_form():
    return render_template('email_form.html')

@app.route('/send_email_submit', methods=['POST'])
def send_email_submit():
    try:
        correo_user = request.form['correo_user']
        correo_send = request.form['correo_send']
        asunto = request.form.get('asunto', 'Prueba')
        mensaje = request.form.get('mensaje', 'Esto es una prueba')
        
        correo = yagmail.SMTP(correo_user, token)
        
        correo.send(
            to=correo_send,
            subject=asunto,
            contents=mensaje,
            headers={
                'From': f'Aplicación Web <{correo_user}>'
            },
            attachments=["raton.png"]
        )
        
        return render_template('email_success.html', 
                              correo_destino=correo_send)
    
    except Exception as e:
        return render_template('email_error.html', 
                              error=str(e))

if __name__ == '__main__':
    app.run(debug=True)