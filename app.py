from flask import Flask, render_template, request, redirect, url_for
import boto3
import uuid
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
db.init_app(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(100))
    file_url = db.Column(db.String(200))
    # bucket = db.Column(db.String(100))
    # region = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        uploaded_file = request.files["new-file"]
        if not allowed_file(uploaded_file.filename):
            return "FILE NOT ALLOWED!"

        new_filename = uuid.uuid4().hex + '.' + uploaded_file.filename.rsplit('.', 1)[1].lower()

        bucket_name = "4myachubucket"
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).upload_fileobj(uploaded_file,new_filename)
        file_url = 'https://4myachubucket.s3.us-east-2.amazonaws.com/{}'.format(new_filename)
        new_file = File(filename = new_filename, file_url = file_url)
        # query = db.insert(File).values(filename=new_filename, file_url=achufile)
        db.session.add(new_file)
        db.session.commit()
        return redirect(url_for('index'))

    # Get the files from de db   
    files = File.query.all()

    return render_template('index.html', files=files)

if __name__ == "__main__":
    app.run(debug=True)
