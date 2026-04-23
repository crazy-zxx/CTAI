import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
import torch
from flask import *
import core.main
import core.net.unet as net

# 导入数据库管理类
from database import db


# 设置 pytorch 的 pth 模型路径
model_path = "../CTAI_model/best_unet_model.pth"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

ALLOWED_EXTENSIONS = set(['dcm'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = './uploads'

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/ct')
        image_path = os.path.join('./tmp/ct', file.filename)

        # 获取患者信息
        patient_id = request.form.get('patient_id')
        name = request.form.get('name')
        gender = request.form.get('gender')
        age = request.form.get('age')
        phone = request.form.get('phone')
        body_part = request.form.get('body_part')

        # 构建患者数据
        patient_data = {
            'patient_id': patient_id,
            'name': name,
            'gender': gender,
            'age': age,
            'phone': phone,
            'body_part': body_part
        }

        # 添加患者（如果不存在）并获取患者ID
        patient_id_in_db = db.add_patient(patient_data)

        # 调用推理函数
        pid, image_info = core.main.c_main(image_path, current_app.model)

        # 构建诊断数据
        diagnosis_data = {
            'ct_image_path': src_path,
            'original_image_url': 'http://127.0.0.1:5003/tmp/image/' + pid,
            'annotated_image_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
            'area': float(image_info['area'][1]) if 'area' in image_info else 0,
            'perimeter': float(image_info['perimeter'][1]) if 'perimeter' in image_info else 0,
            'focus_x': float(image_info['focus_x'][1]) if 'focus_x' in image_info else 0,
            'focus_y': float(image_info['focus_y'][1]) if 'focus_y' in image_info else 0,
            'ellipse': float(image_info['ellipse'][1]) if 'ellipse' in image_info else 0,
            'mean': float(image_info['mean'][1]) if 'mean' in image_info else 0,
            'std': float(image_info['std'][1]) if 'std' in image_info else 0,
            'piandu': float(image_info['piandu'][1]) if 'piandu' in image_info else 0,
            'fengdu': float(image_info['fengdu'][1]) if 'fengdu' in image_info else 0,
            'small_grads_dominance': float(image_info['small_grads_dominance'][1]) if 'small_grads_dominance' in image_info else 0,
            'big_grads_dominance': float(image_info['big_grads_dominance'][1]) if 'big_grads_dominance' in image_info else 0,
            'gray_asymmetry': float(image_info['gray_asymmetry'][1]) if 'gray_asymmetry' in image_info else 0,
            'grads_asymmetry': float(image_info['grads_asymmetry'][1]) if 'grads_asymmetry' in image_info else 0,
            'energy': float(image_info['energy'][1]) if 'energy' in image_info else 0,
            'gray_mean': float(image_info['gray_mean'][1]) if 'gray_mean' in image_info else 0,
            'grads_mean': float(image_info['grads_mean'][1]) if 'grads_mean' in image_info else 0,
            'gray_variance': float(image_info['gray_variance'][1]) if 'gray_variance' in image_info else 0,
            'grads_variance': float(image_info['grads_variance'][1]) if 'grads_variance' in image_info else 0,
            'corelation': float(image_info['corelation'][1]) if 'corelation' in image_info else 0,
            'gray_entropy': float(image_info['gray_entropy'][1]) if 'gray_entropy' in image_info else 0,
            'grads_entropy': float(image_info['grads_entropy'][1]) if 'grads_entropy' in image_info else 0,
            'entropy': float(image_info['entropy'][1]) if 'entropy' in image_info else 0,
            'inertia': float(image_info['inertia'][1]) if 'inertia' in image_info else 0,
            'differ_moment': float(image_info['differ_moment'][1]) if 'differ_moment' in image_info else 0
        }

        # 添加诊断记录
        db.add_diagnosis(patient_id_in_db, diagnosis_data)

        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/image/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info
                        })


    return jsonify({'status': 0})


@app.route("/download", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory('data', 'testfile.zip', as_attachment=True)


# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    # print(file)
    if request.method == 'GET':
        if file is None:
            pass
        else:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass


# 获取患者信息
@app.route('/get_patient_info', methods=['GET'])
def get_patient_info():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'status': 0, 'message': '请提供患者ID'})

    # 查询患者信息
    patient = db.get_patient(patient_id)

    if patient:
        patient_info = {
            'patient_id': patient['patient_id'],
            'name': patient['name'],
            'gender': patient['gender'],
            'age': patient['age'],
            'phone': patient['phone'],
            'body_part': patient['body_part']
        }
        return jsonify({'status': 1, 'patient': patient_info})
    else:
        return jsonify({'status': 0, 'message': '未找到该患者信息'})

# 获取历史诊断数据
@app.route('/get_history_diagnoses', methods=['GET'])
def get_history_diagnoses():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'status': 0, 'message': '请提供患者ID'})

    # 查询患者信息
    patient = db.get_patient(patient_id)

    if not patient:
        return jsonify({'status': 0, 'message': '未找到该患者信息'})

    # 查询该患者的所有诊断记录
    diagnoses = db.get_patient_diagnoses(patient_id)

    if diagnoses:
        # 对于每个诊断记录，获取完整的特征信息
        diagnosis_list = []
        for diagnosis in diagnoses:
            # 获取完整的诊断特征
            diagnosis_features = db.get_diagnosis_features(diagnosis['id'])
            if diagnosis_features:
                # 合并基本信息和特征信息
                diagnosis_info = {
                    'id': diagnosis['id'],
                    'patient_id': patient['id'],
                    'diagnosis_date': diagnosis['diagnosis_date'],
                    'ct_image_path': diagnosis.get('ct_image_path'),
                    'original_image_url': diagnosis.get('original_image_url'),
                    'annotated_image_url': diagnosis.get('annotated_image_url'),
                    **diagnosis_features
                }
                diagnosis_list.append(diagnosis_info)

        if diagnosis_list:
            return jsonify({'status': 1, 'diagnoses': diagnosis_list})
        else:
            return jsonify({'status': 0, 'message': '未找到该患者的历史诊断数据'})
    else:
        return jsonify({'status': 0, 'message': '未找到该患者的历史诊断数据'})

# 获取患者历史数据API
@app.route('/get_history_data', methods=['POST'])
def get_history_data():
    # 获取请求数据
    data = request.json
    patient_id = data.get('patient_id')

    if not patient_id:
        return jsonify({'status': 0, 'message': '请提供患者ID'})

    # 查询患者信息
    patient = db.get_patient(patient_id)

    if not patient:
        return jsonify({'status': 0, 'message': '未找到该患者信息'})

    # 查询患者的历史诊断数据
    diagnoses = db.get_patient_diagnoses(patient_id)

    if not diagnoses:
        return jsonify({'status': 0, 'message': '未找到该患者的历史诊断数据'})

    # 构建患者信息和历史诊断数据
    patient_info = {
        'patient_id': patient['patient_id'],
        'name': patient['name'],
        'gender': patient['gender'],
        'age': patient['age'],
        'body_part': patient['body_part']
    }

    diagnosis_history = []
    for diagnosis in diagnoses:
        # 获取完整的诊断特征
        diagnosis_features = db.get_diagnosis_features(diagnosis['id'])
        if diagnosis_features:
            # 合并基本信息和特征信息
            diagnosis_info = {
                'id': diagnosis['id'],
                'patient_id': patient['id'],
                'diagnosis_date': diagnosis['diagnosis_date'],
                'ct_image_path': diagnosis.get('ct_image_path'),
                'original_image_url': diagnosis.get('original_image_url'),
                'annotated_image_url': diagnosis.get('annotated_image_url'),
                **diagnosis_features
            }
            diagnosis_history.append(diagnosis_info)

    if not diagnosis_history:
        return jsonify({'status': 0, 'message': '未找到该患者的历史诊断数据'})

    return jsonify({'status': 1, 'patient_info': patient_info, 'diagnosis_history': diagnosis_history})


def init_model():
    model = net.Unet(1, 1).to(device)
    if torch.cuda.is_available():
        model.load_state_dict(torch.load(model_path))
    else:
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    return model


if __name__ == '__main__':

    # 创建需要的临时目录
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('./tmp/ct', exist_ok=True)
    os.makedirs('./tmp/image/', exist_ok=True)
    os.makedirs('./tmp/mask/', exist_ok=True)
    os.makedirs('./tmp/draw/', exist_ok=True)

    # 创建数据库
    db.init_database()

    with app.app_context():
        current_app.model = init_model()
    app.run(host='127.0.0.1', port=5003, debug=True)
