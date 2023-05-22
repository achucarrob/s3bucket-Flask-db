from flask import Flask, render_template, request, redirect, url_for
import boto3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
db.init_app(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    bucket = db.Column(db.String(100))
    region = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        uploaded_file = request.files['new-file']
        if uploaded_file == "":
            return 'please select a file'

        bucket_name = "4myachubucket"
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).upload_fileobj(uploaded_file, bucket_name)

        return redirect(url_for('index.html'))

    # Get the files from de db   
    files = File.query.all()

    return render_template('index.html', files=files)

if __name__ == "__main__":
    app.run(debug=True)
