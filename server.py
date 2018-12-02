from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result():
    print("In function")
    print(request.form)
    values=dict(request.form.items())
    print(values)
    return render_template('result.html', values=values)

if __name__ == '__main__':
    app.run(debug=True)