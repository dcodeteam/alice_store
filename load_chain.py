import json

import yaml

import utils


def register_hams_in_chain():
    for ham in utils.HAMSTERS:
        utils.rds.set(ham['id'], ham['data'])
        utils.rds.lpush('ham_list', ham['id'])
        data = {
            'jobs':
                [{'name': 'storeHams',
                  'call':
                      {
                          'destination': '15689BB829CB79ED7C392191445B385FE4696A5B',
                          'function': 'reg_hams',
                          'data': [json.dumps(ham)]
                          }
                  }]
        }
        with open('alice_store.yaml', 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

        utils.run_burrow_store()
        _hash = utils.read_chain_value('storeHams', 'alice_store.output.json')
        utils.rds.set(_hash, ham['id'])


"""Supposed to be used by super permission access, separately"""
if __name__ == '__main__':
    register_hams_in_chain()
