from flask import Flask
from flask import render_template, request
import random

app = Flask(__name__)


@app.route('/generator', methods=['get', 'post'])
def generator():
    genders = ["цисгендер", "бигендер", "демигендер", "гендерфлюид", "демифлюид", "трансгендер", "агендер", "пангендер"]
    sexs = ["гомосексуальность", "гетеросексуальность", "бисексаульность", "асексуальность",
            "пансексуальность", "демисексуальность", "полисексуальность"]
    rom = ["панромантик", "гетероромантик", "биромантик", "аромантик",
           "андроромантик", "гинеромантик", "грейромантик", "демиромантик", "гоморомантик"]
    if request.method == 'POST':
        return render_template('gen.html',
                               response=True,
                               gender=random.choice(genders),
                               sexuality=random.choice(sexs),
                               romantic=random.choice(rom))
    return render_template('gen.html')



if __name__ == '__main__':
    app.run(debug=True)
