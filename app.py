from datetime import datetime, timedelta

from flask import Flask , render_template , request , redirect , jsonify , session
import pymysql
import hashlib
import bcrypt
import jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, create_access_token, get_jwt_identity, get_jwt_claims)


app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'secret'
# jwt = JWTManager(app)
app.config.update(
    DEBUG = True ,
    JWT_SECRET_KEY = 'secret'
)
jwt = JWTManager(app)
db = pymysql.connect(host = 'localhost' , port = 3306 , user = 'root' , passwd = '8813' , db = 'hackaton' , charset = 'utf8') # db 접속 본인 환경맞춰 설정
cursor = db.cursor() # 객체에 담기

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
    if 'email' in session:
        return render_template('mypage.html')
    else:
        return redirect('/loginpage')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/login' , methods=['POST'])
def login():
    if request.method == 'POST':
        login_info = request.form

        email = login_info['email']
        password = login_info['password']
        print(email + password)
        sql = "SELECT * FROM Userinfo WHERE email = %s"
        rows_count = cursor.execute(sql , email)
        if rows_count > 0:
            user_info = cursor.fetchone() # 일치하는 정보 객체에 담기
            print("user info : " , user_info)
            is_pw_correct = bcrypt.checkpw(password.encode('UTF-8') , user_info[2].encode('UTF-8')) # 패스워드 맞는지 확인
            if is_pw_correct: # 일치하게되면
                session['email'] = email
            else: # 비밀번호가 일치하지 않는다면
                return redirect('/loginpage')
        else:
            print('User does not exist')
            return redirect('/loginpage')

@app.route('/registerpage')
def regit():
    return render_template('/register.html')

@app.route('/register' , methods=['POST']) # 회원가입부분
def register():
    if(request.method == 'POST'):
        register_info = request.form
        email = register_info['email']
        hased_password = bcrypt.hashpw(register_info['password'].encode('utf-8') , bcrypt.gensalt())
        name = register_info['name']
        department = register_info['department']
        sno = register_info['sno']
        sex = register_info['sex']

        sql = """
            INSERT INTO Userinfo (email, hashed_password, name, sex, department, student_number) VALUES (%s , %s , %s , %s, %s, %s);
        """
        # 아이디 겹치면 try 구문 사용해서 오류 반환해주기 ... 구현해야함
      #  cursor.execute(sql , (username , hased_password, email , department)) # sql 실행
        print(register_info)
        cursor.execute(sql , (email , hased_password , name , sex, department, sno))
        db.commit() #데이터 삽입 , 삭제 등의 구문에선 commit 해주어야함

        db.close() # 연결 해제        return redirect(request.url)
    return render_template('/login.html')
#---------------------------------------------------------

    
if __name__ == '__main__':
    app.run(debug=True)