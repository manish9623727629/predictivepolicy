from flask import Flask,render_template,request,session,redirect,url_for
from flask_session import Session as appSession
import psutil,os
from forms import InfoForm
import secrets
from flask_wtf.csrf import CSRFProtect
# from getGPU import openclInfo
# import tensorflow as tf
# import GPUtil


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.update(dict(
    SECRET_KEY=secrets.token_hex(16),
    WTF_CSRF_SECRET_KEY=secrets.token_hex(16),
    SESSION_PERMANENT=False,
    SESSION_TYPE='filesystem',
    SESSION_FILE_DIR='/tmp'
))
appSession(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = InfoForm(request.form)
    if request.method == 'POST':
        if session.get('config',''):
            session.pop('config')
        app_type = request.form.get('app_type')
        input_cpu = request.form['cpu']
        input_ram = request.form['ram']
        input_memory = request.form['memory']
        current_cpu,current_ram,current_memory = GetCurrentSystemInfo()
        msg = ''
        if int(input_cpu) <= current_cpu and int(input_ram) <= current_ram and int(input_memory) <= current_memory:
            msg = f'{input_cpu} CPU cores, {input_ram}GB RAM , {input_memory}GB Disk will be alloctaed'
            success = True
        else:
            success = False
            if int(input_cpu) > current_cpu:
                msg += f'Only {current_cpu} CPU cores can be alloctaed, \n'
            if int(input_ram) > current_ram:
                msg += f'Only {current_ram}GB RAM can be alloctaed, \n'
            if int(input_memory) > current_memory:
                msg += f'Only {current_memory}GB Disk can be alloctaed, \n'
        result = {
            'app_type':f'{app_type}',
            'msg':f'{msg}',
            'success': success,
            'cpu':input_cpu,
            'ram':input_ram,
            'memory':input_memory
        }
        session['config'] = result
        return render_template('script.html',result=result,form=form)
    return render_template('index.html',form=form)

@app.route('/openContainer', methods=['POST'])
def openContainer():
    if request.method == 'POST':
        containers = request.form['no_of_container']
        config_info = session['config']
        print(containers,config_info)
        return redirect(url_for('home'))

def GetCurrentSystemInfo():
    cpu = psutil.cpu_count()
    ram = round(psutil.virtual_memory().free/(1024 * 1024 * 1024), 2)
    disk = round(psutil.disk_usage(os.getcwd()).free/(1024 * 1024 * 1024), 2)
    return cpu,ram,disk

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=80)
