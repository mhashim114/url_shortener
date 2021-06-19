from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'masb6t7wcjbw78y7'


@app.route('/')
def home():
    return render_template('home.html', codes = session.keys())


@app.route('/your-url', methods = ['GET', 'POST'])
def your_url():
    if  request.method == 'POST':
        url ={}

        if os.path.exists('url_collections.json'):
             with open('url_collections.json') as url_file:
                 url = json.load(url_file)
        
        if request.form['code'] in url.keys():
            flash('This short name has already benn taken. Please select a new one.')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            url[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename) 
            f.save('D:/Courses/Flask/url_shortener/static/user_files/' + full_name)
            url[request.form['code']] = {'file': full_name}
        
        with open('url_collections.json', 'w') as url_file:
            json.dump(url, url_file)
            session[request.form['code']] = True

        return render_template('your_url.html', code = request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_url(code):
    if os.path.exists('url_collections.json'):
        with open('url_collections.json') as url_file:
            urls = json.load(url_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename = 'user_files/' + urls[code]['file']))
    
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))



if __name__ == "__main__":
      app.run(host='127.0.0.1', port=8000, debug=True)