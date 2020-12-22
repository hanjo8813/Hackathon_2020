from flask import Flask , render_template, redirect


app = Flask(__name__)

# 처음 index 시작 ----------------------------------------
@app.route('/')
def index():
    return render_template('index.html')
# 상단 메뉴바 href ----------------------------------------
@app.route('/logo_index')
def logo_index():
    return render_template('index.html')

@app.route('/teamplay')
def teamplay():
    return render_template('teamplay.html')

@app.route('/outsourcing')
def outsourcing():
    return render_template('outsourcing.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

@app.route('/login')
def login():
    return render_template('login.html')
#---------------------------------------------------------

    
if __name__ == '__main__':
    app.run(debug=True)