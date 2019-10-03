from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", title="Checklist")

# @app.route("/setup", methods=["POST"])
# def setup():
#     check here if name is already taken
#     save credentails 
#     and redirect to site which allows editing of checklist

if __name__ == '__main__':
    app.run()