#!/usr/bin/env python
import optparse

from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'GET':
        return render_template('landing.html')
    elif request.method == 'POST':
        return redirect(url_for('nanny', target_url=request.form['url']),
                code=303)


@app.route('/<path:target_url>', methods=['GET', 'POST'])
def nanny(target_url):
    if request.method == 'GET':
        if request.cookies.get('accepted') is not None:
            return redirect(target_url)
        else:
            return render_template('nanny.html')
    elif request.method == 'POST':
        resp = redirect(target_url, code=303)
        if request.form.get('persist', None) is not None:
            # 86400 seconds is equal to 24 hours
            resp.set_cookie('accepted', 'true', max_age=86400)
        return resp


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-d', '--debug', action='store_true', dest='debug',
            default=False,
            help="enable Flask's debugging options [default: off]")
    parser.add_option('-p', '--port', action='store', dest='port',
            type='int', default=8080,
            help='which port to listen on [default: %default]')
    parser.add_option('-l', '--listen', action='store', dest='listen_addr',
            default='127.0.0.1',
            help='which address to listen on [default: %default]')
    (opts, args) = parser.parse_args()
    app.debug = opts.debug
    app.run(host=opts.listen_addr, port=opts.port)
