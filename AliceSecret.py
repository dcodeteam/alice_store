import json

import flask
import yaml
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import utils

app = Flask(__name__)
bootstrap = Bootstrap(app)
cache = utils.rds
PAGE_LIMIT = 5


@app.route('/burrow/demo/')
def index():
    hams = cache.lrange('ham_list', 0, -1)
    ham_data = []
    for ham_id in hams:
        data = cache.get(ham_id)
        data = data.decode('utf-8')
        data = json.loads(data.replace("'", '"'))

        ham_data.append({'id': ham_id.decode('utf-8'), 'data': data})

    return render_template('index.html', data=ham_data)


@app.route('/burrow/demo/info/<ham_id>')
def info_ham(ham_id):
    ham_info = cache.get(ham_id)
    if ham_info:
        ham_info = ham_info.decode('utf-8')
        ham_info = json.loads(ham_info.replace("'", '"'))

    return flask.jsonify(ham_info)


@app.route('/burrow/demo/delete/<ham_id>')
def delete_ham(ham_id):
    cache.delete(ham_id)
    cache.lrem('ham_list', 0, ham_id)
    ctx = {'msg': 'Ham with ID: {} deleted, refresh the page'.format(ham_id)}
    return flask.jsonify(ctx)


@app.route('/burrow/demo/update/<ham_id>', methods=['POST'])
def update_ham(ham_id):
    jsn_ham = flask.request.get_json()
    cache.set(ham_id, jsn_ham)

    ctx = {'msg': 'Ham with ID: {} updated, refresh the page'.format(ham_id)}
    return flask.jsonify(ctx)


@app.route('/burrow/demo/validate/<ham_id>')
def validate_ham(ham_id):
    ham_data = cache.get(ham_id)
    ham_data = ham_data.decode('utf-8') if ham_data else None
    is_vld = False
    if ham_data:
        ham_data = {'id': int(ham_id),
                     'data': json.loads(ham_data.replace("'", '"'))}
        data = {
            'jobs':
                [{'name': 'validHams',
                  'call':
                    {'destination': '557B709A0C8009FCC15CA8E8546482496F2F60B2',
                     'function': 'vld_hams',
                     'data': [json.dumps(ham_data)]
                     }
                  }]
        }
        with open('alice_store_validate.yaml', 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

            """Run for blockchain check data hash integrity"""
            utils.run_burrow_validity()

            """Read for returned values from blockchain"""
            is_vld = utils.read_chain_value('validHams',
                                            'alice_store_validate.output.json')

    return flask.jsonify({'is_valid': is_vld})


@app.route('/burrow/demo/check/data')
def check_hams_integrity():
    """Run for blockchain check data hash integrity"""
    utils.run_burrow_integrity()

    """Read for returned values from blockchain"""
    hash_vls = utils.read_chain_value('checkHams',
                                      'alice_store_integrity.output.json')

    ctx = {'msg': 'Error occurred while chain scanning', 'err': False}
    for val in hash_vls.split(','):
        val = val.strip('[]')
        ham_id = cache.get(val)
        if ham_id and cache.get(ham_id):
            ctx = {'msg': 'All data in place', 'err': False}
        else:
            ctx = {'msg': 'Data with hash value {} are missed'.format(val),
                   'err': True}
            break

    return flask.jsonify(ctx)


if __name__ == '__main__':
    app.run(debug=True)
