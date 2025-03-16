# 相關套件
from flask import Flask, render_template,request

from scraper import search

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    if request.method =="POST":
        keyword = request.form.get("keyword")
        res_list =search(keyword)
        print(keyword)
        return render_template('result.html', res_list=res_list, keyword=keyword)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)