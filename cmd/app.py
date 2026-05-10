from flask import Flask, render_template


app = Flask(__name__, template_folder='../templates')


TEXT = '''
Привет это текстовое приложение
для знакомства с фласком
и шаблонизатором Джинджа!
'''

studnets = [
    {'name:' : 'Костя', 'age' : '25'},
    {'name:' : 'Никита', 'age' : '19'},
    {'name:' : 'Дима', 'age' : '14'}
]



@app.route('/')
def base():
    return render_template('base.html', dis_text=TEXT, students=studnets)






if __name__ == "__main__":
    app.run()