#!/usr/bin/env python
from flask import Flask, request, url_for, make_response, redirect, render_template

app = Flask(__name__)

@app.route('/<path:target_url>', methods=['GET', 'POST'])
def gate(target_url):
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
    app.run()
