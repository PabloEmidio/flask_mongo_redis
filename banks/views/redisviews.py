from flask import Flask, redirect, jsonify, abort, request
from pymongo import database

from banks.models.models import RedisDatabaseModel
from banks.models.sample_banks import REDIS_SAMPLE_BANKS

database = RedisDatabaseModel()

def init_app(app: Flask):

    @app.route('/redis/')
    def redis_add_sample_banks():
        if not database.get_keys():
            for i in range(0, len(REDIS_SAMPLE_BANKS), 2):
                database.insert(REDIS_SAMPLE_BANKS[i], REDIS_SAMPLE_BANKS[i+1])
        return redirect('/redis/banks/')

    @app.route('/redis/banks/', methods=['GET', 'POST'])
    def redis_list_banks():
        if request.method == 'GET':
            values = database.get_values()
            if not values:
                return redirect('/redis/')
            banks, status_code = [], 200
            for pos, value in enumerate(values):
                if pos%2==0:
                    banks.append(value)
                else:
                    banks[-1]['infos'] = {
                        'is_digital': bool(int(value['is_digital'])),
                        'website': value['website'],
                        'has_investment_platform': bool(int(value['has_investment_platform']))
                    }
        else:
            try:
                assert_message = 'Document must have {}'
                bank_fields, status_code = request.json, 201
                assert isinstance(bank_fields, dict), assert_message.format('only one')
                assert 'bank' in bank_fields.keys(), assert_message.format('bank')
                assert 'pop_name' in bank_fields.keys(), assert_message.format('pop_name')
                assert 'cod' in bank_fields.keys(), assert_message.format('cod')
                assert 'infos' in bank_fields.keys(), assert_message.format('infos')
                assert 'is_digital' in bank_fields['infos'].keys(), assert_message.format('infos.is_digital')
                assert 'website' in bank_fields['infos'].keys(), assert_message.format('infos.website')
                bank_infos = bank_fields['infos']
                bank_infos = {
                    'is_digital': 1 if bank_infos['is_digital'] else 0,
                    'website': bank_infos['website'],
                    'has_investment_platform': 1 if bank_infos['has_investment_platform'] else 0
                }
                bank_fields.pop('infos')
                database.insert(bank_fields, bank_infos)
                return redirect(f'/redis/{bank_fields["cod"]}/', 303)
            except AssertionError as error:
                status_code = 400
                banks = {
                    'message': str(error),
                    'status_code': status_code
                }
            except Exception as error:
                print(error)
                abort(500)
        return jsonify(banks), status_code

    @app.route('/redis/<cod>/', methods=['GET', 'DELETE', 'PUT'])
    def redis_bank_by_cod(cod):
        bank_key, info_key = f'banks:{cod}', f'banks:{cod}:infos'
        if request.method == 'GET':
            try:
                values = database.get_values(bank_key, info_key)
                assert values[0] and values[1], ''
                bank = values[0]
                bank['infos'] = {
                    'is_digital': bool(int(values[1]['is_digital'])),
                    'website': values[1]['website'],
                    'has_investment_platform': bool(int(values[1]['has_investment_platform']))
                }
            except AssertionError:
                abort(404)
            except Exception:
                abort(500)

        if request.method == 'PUT':
            try:
                update_assert_message = 'An error happened updating {}'
                bank, status_code = request.json, 201
                assert isinstance(bank, dict), 'Just updated one document'
                assert 'bank' not in bank.keys(), 'Field bank cannot be changed'
                assert 'cod' not in bank.keys(), 'Field cod cannot be changed'

                if pop_name := bank.get('pop_name'):
                    assert isinstance(pop_name, str), 'pop_name must be string'
                    assert database.update(
                        bank_key, {'pop_name': pop_name}
                    ), update_assert_message.format('pop_name')
                
                if infos := bank.get('infos'):
                    if is_digital := infos.get('is_digital'):
                        assert isinstance(is_digital, bool), 'is_digital must be boolean'
                        is_digital = 1 if is_digital else 0
                        assert database.update(
                            info_key, {'is_digital': is_digital}
                        ), update_assert_message.format('is_digital')

                    if website := infos.get('website'):
                        assert isinstance(website, str), 'website must be boolean'
                        assert database.update(
                            info_key, {'website': website}
                        ), update_assert_message.format('website')

                    if hip := infos.get('has_investment_platform'):
                        assert isinstance(hip, bool), f'{hip} must be boolean'
                        hip = 1 if hip else 0
                        assert database.update(
                            info_key, {'has_investment_platform': hip}
                        ), update_assert_message.formaftf(f'{hip}')
                print(infos)
                return redirect(f'/redis/{cod}/')
            except AssertionError as error:
                status_code = 400
                bank = {
                    'message': str(error),
                    'status_code': status_code
                }
            except Exception as error:
                print(error)
                abort(500)

        if request.method == 'DELETE':
            try:
                assert database.delete(bank_key, info_key), ''
                return redirect('/redis/banks/')
            except AssertionError:
                abort(404)
            except Exception:
                abort(500)
        return bank

