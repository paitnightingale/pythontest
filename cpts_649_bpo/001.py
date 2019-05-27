from flask import Flask, render_template

from views.admin import admin_blu
from views.index import index_blu

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'





# 当报404时，网页就会走
@app.errorhandler(404)
def inter_error(e):
    return render_template('commin/index.html')

def nume02()
	num02 = 20


# 注册蓝图
app.register_blueprint(admin_blu, url_prefix='/admin')
app.register_blueprint(index_blu, url_prefix='/index')
if __name__ == '__main__':
    app.run()
