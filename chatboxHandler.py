from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'


@app.route('/', methods=['POST', 'GET'])
def postPrompt():
    if request.method == 'POST':
        userPrompt = request.form.get('userPrompt')
        return redirect(url_for('verify'))
    
    return render_template('chat.html')

@app.route('/verify')
def verify():
    return render_template('verify.html')




if __name__ == '__main__':
