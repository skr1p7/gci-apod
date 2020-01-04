from flask import Flask, render_template, request, redirect, url_for
import requests
import wget
from docx import Document
from docx.shared import Inches
import os


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    if request.method == "POST":
        flag = 0
        date = request.form['text']
        global url
        url = 'https://api.nasa.gov/planetary/apod?api_key=w43FMRhURuPXm5zO3mYsSa4pBJMfcH3CggwfyeZZ&date={}'.format(date)
        req = requests.get(url)
        data = req.json()
        if req.status_code == 400:
            return render_template('error.html')
        else:
            pass
        img = data['hdurl']
        title = data['title']
        return render_template('index.html',image=img, title=title)
    else:
        return render_template('base.html')

@app.route('/download/', methods=['GET','POST'])
def download():
    data = requests.get(url).json()
    imgUrl = data['hdurl']
    imgTitle = data['title']
    filename = wget.download(imgUrl)
    a = "File downloaded as " + filename
    #pdf = canvas.Canvas('mypdf', pagesize=A4)
    #pdf.setTitle(filename)
    #pdf.drawCentredString(270, 770, str(imgTitle))
    #pdf.drawInlineImage( str(filename), 1, 1,width=530,preserveAspectRatio=True)
    #pdf.save()

    document = Document()
    document.add_heading(str(imgTitle), 0)
    document.add_picture(str(filename), width=Inches(6))
    document.add_page_break()
    document.save('file.docx')
    os.system('libreoffice --convert-to pdf file.docx')

    
    return render_template('downloaded.html', a=a)

if __name__ == "__main__":
    app.run()