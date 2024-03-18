from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL
from pytube import YouTube

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'  # Sua chave secreta

class VideoForm(FlaskForm):
    video_url = StringField('URL do vídeo do YouTube', validators=[URL()])
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoForm()
    video_info = None
    video_streams = None
    download_link = None

    if form.validate_on_submit():
        video_url = form.video_url.data
        try:
            yt = YouTube(video_url)
            video_info = {
                'title': yt.title,
                'author': yt.author,
                'thumbnail_url': yt.thumbnail_url,
            }
            video_streams = yt.streams.filter(progressive=True)
        except Exception as e:
            return render_template('error.html', error=str(e))

    return render_template('index.html', form=form, video_info=video_info, video_streams=video_streams, download_link=download_link)

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            stream.download()
            download_link = stream.default_filename
            return redirect(url_for('index', download_link=download_link))
        except Exception as e:
            return render_template('error.html', error=str(e))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
