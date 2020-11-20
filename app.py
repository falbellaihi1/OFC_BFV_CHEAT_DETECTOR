import http.client
import json
import os

from flask import Flask, jsonify

from auth import get_headers

app = Flask(__name__)

API_DOMAIN = os.environ.get('API_DOMAIN')


def weapon_data_helper(player_origin_name):
    headers = get_headers()
    conn = http.client.HTTPSConnection(API_DOMAIN)
    payload = "{\"query\":\"\",\"variables\":{}}"
    conn.request("GET", "/api/v1/bfv/profile/origin/{}/weapons".
                 format(player_origin_name),
                 payload, headers)
    res = conn.getresponse()
    data = res.read()
    player_weapons_loads = json.loads(data)
    weapons = player_weapons_loads['data']['children']
    weapons_stats = []
    for i in range(len(weapons)):
        '''displays player weapons stats'''
        weapons_stats.append(
            {
                "weapons_stats": {
                    weapons[i]['metadata']['name']: {
                        # dirty work around for now
                        weapons[i]['stats'][0]['metadata']['key']:
                            weapons[i]['stats'][0]['displayValue'],
                        weapons[i]['stats'][1]['metadata']['key']:
                            weapons[i]['stats'][1]['displayValue'],
                        weapons[i]['stats'][2]['metadata']['key']:
                            weapons[i]['stats'][2]['displayValue'],
                        weapons[i]['stats'][3]['metadata']['key']:
                            weapons[i]['stats'][3]['displayValue'],
                        weapons[i]['stats'][4]['metadata']['key']:
                            weapons[i]['stats'][4]['displayValue'],
                        weapons[i]['stats'][5]['metadata']['key']:
                            weapons[i]['stats'][5]['displayValue'],
                        weapons[i]['stats'][6]['metadata']['key']:
                            weapons[i]['stats'][6]['displayValue'],

                    },

                }
            }
        )
    return weapons_stats


def game_reports_helper(player_origin_name): #TODO
    reports_dic = []
    headers = get_headers()
    conn = http.client.HTTPSConnection(API_DOMAIN)
    payload = "{\"query\":\"\",\"variables\":{}}"
    conn.request("GET", "/api/v1/bfv/gamereports/origin/latest/{}".format(
        player_origin_name),
                 payload, headers)
    res = conn.getresponse()
    data = res.read()

    # data_uni = (data.decode("utf-8"))
    json_loads = json.loads(data)
    report_id = json_loads['data']['reports']
    for id in range(len(report_id)):
        reports_dic.append(report_id[id]['gameReportId'])
    return reports_dic

@app.route('/player/stats/<player_origin_name>')
def get_player_data(player_origin_name):
    headers = get_headers()
    conn = http.client.HTTPSConnection(API_DOMAIN)
    payload = "{\"query\":\"\",\"variables\":{}}"
    conn.request("GET", "/api/v2/bfv/standard/profile/origin/{}".format(
        player_origin_name),
                 payload, headers)
    res = conn.getresponse()
    data = res.read()
    # data_uni = (data.decode("utf-8"))
    json_loads = json.loads(data)

    return jsonify({
        "success": True,
        "data": json_loads
    })


@app.route('/player/weapons/<player_origin_name>', methods=['GET'])
def get_player_weapon_data(player_origin_name):
    """
    a function that returns player weapon stats
    :param player_origin_name:
    :return: players' weapon stats
    """

    return jsonify({
        "success": True,
        "data": weapon_data_helper(player_origin_name)
    })



@app.route('/player/reports/<player_origin_name>', methods=['GET'])
def get_player_game_reports(player_origin_name):
    headers = get_headers()
    conn = http.client.HTTPSConnection(API_DOMAIN)
    payload = "{\"query\":\"\",\"variables\":{}}"
    conn.request("GET", "/api/v1/bfv/gamereports/origin/latest/{}".format(
        player_origin_name),
                 payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_loads = json.loads(data)
    test = game_reports_helper(player_origin_name)
    return jsonify({
        "success": True,
        "data": json_loads
    })

@app.route('/player/reports/id/<report_id>', methods=['GET'])
def get_player_game_reports_id(report_id):
    headers = get_headers()
    conn = http.client.HTTPSConnection(API_DOMAIN)
    payload = "{\"query\":\"\",\"variables\":{}}"
    conn.request("GET",
                 "/api/v1/bfv/gamereports/origin/direct/1329558794147715072",
                 payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_loads = json.loads(data)


    return jsonify({
        "success": True,
        "data": json_loads
    })


@app.route('/player/weapons/RPM/<player_origin_name>', methods=['GET']) #TODO, STILL STUDYING
def cheat_RPM(player_origin_name):
    weapons = weapon_data_helper(player_origin_name)
    total_kills_in_all_weapons = 0
    shot_accurcy = 0
    RPM = 0;
    for i in range(len(weapons)):
        for key in weapons[i]['weapons_stats']:
            print("shotsAccuracy",
                  weapons[i]['weapons_stats'][key]['shotsAccuracy'])
            print(key, "HEAD SHOTS :",
                  weapons[i]['weapons_stats'][key]['headshots'])
            total_kills_in_all_weapons += int(
                weapons[i]['weapons_stats'][key]['headshots'])
            print(total_kills_in_all_weapons)




    return jsonify({
        "success": True,
        "data": weapons
    })


if __name__ == '__main__':
    app.run()
