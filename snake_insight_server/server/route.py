import json
import pickle
import time

from loguru import logger

from random_forest.utils.place_code import region_code, area_code
from snake_insight_server.server import request, make_response, Filter
from snake_insight_server.classes import Query, Calculator
from flask import Flask, request, make_response

from snake_insight_threading.common import PredictByType
from random_forest import space_random_forest, price_random_forest

app = Flask(__name__)
filter = Filter()


# http://localhost:19198/plot
@app.route('/plot', methods=["GET", "POST"])
def get_info():
    start = time.time()
    params = request.json
    raw_response = {}
    if isinstance(params, dict):
        try:
            loc = params.get("loc", [])
            if isinstance(loc, str):
                loc = [loc]
            elif not isinstance(loc, list):
                raise Exception("loc")

            x_field = params["x"]
            if not isinstance(x_field, str):
                raise Exception("x")

            y_fields = []
            if not isinstance(params["ys"], list):
                raise Exception("ys")
            for y in params["ys"]:
                if isinstance(y, list) and len(y) == 2:
                    y_fields.append((y[0], y[1], False))
                elif isinstance(y, list) and len(y) == 3:
                    y_fields.append((y[0], y[1], y[2]))
                else:
                    raise Exception("ys[?]")

            detailed = params.get("detailed", False)
            if not isinstance(detailed, bool):
                raise Exception("detailed")

            _q = Query(*loc, db=1)
            _c = Calculator(query=_q, x_field=x_field, y_fields=y_fields)
            raw_response["plotData"] = _c.plot_data(detailed_data=detailed)

            logger.info(f"Completed. Params: {{loc: {loc}, x: {x_field}, ys: {y_fields}, detailed: {detailed}}}")

        except Exception as e:
            raw_response["message"] = f"Cannot parse request params(Cause: {e})."
    else:
        raw_response["message"] = "Cannot parse request params."

    end = time.time()
    raw_response["process_time"] = {"start": start, "end": end, "cost": end - start}

    response = make_response(json.dumps(raw_response, ensure_ascii=False))
    response.mimetype = 'application/json'

    logger.info(f"Cost {end - start}s")

    return response


@app.route('/getRoomPrice', methods=["GET", "POST"])
def get_room_price():
    params = request.json
    region = params.get("region", "天河")
    logger.info(region)
    raw_response = {}
    res = filter.get_room_price(region)
    processed_res = {}
    for k, v in res.items():
        processed_res[f'{k[1]}室{k[0]}厅'] = v
        v[0] = round(v[0] * 100) / 100

    raw_response["data"] = processed_res
    responce = make_response(json.dumps(raw_response, ensure_ascii=False))
    responce.mimetype = 'application/json'
    return responce


@app.route('/getAreaPrice', methods=["GET", "POST"])
def get_area_price():
    params = request.json
    region = params.get("region", "")
    logger.info(region)
    raw_response = {}
    res = filter.get_area_price(region)
    processed_res = {}
    for k, v in res.items():
        processed_res[k[0]] = v
        v[0] = round(v[0] * 100) / 100

    raw_response["data"] = processed_res
    responce = make_response(json.dumps(raw_response, ensure_ascii=False))
    responce.mimetype = 'application/json'
    return responce


@app.route('/getFloorPrice', methods=["GET", "POST"])
def getFloorPrice():
    params = request.json
    region = params.get("region", "")
    require_elevator = bool(params.get("require_elevator", False))
    logger.info(region)
    raw_response = {}
    res = filter.get_floor_price(require_elevator, region)
    processed_res = {}

    for k, v in res.items():
        processed_res[k[0]] = v
        v[0] = round(v[0] * 100) / 100

    raw_response["data"] = processed_res
    response = make_response(json.dumps(raw_response, ensure_ascii=False))
    response.mimetype = 'application/json'
    return response


@app.route('/getPrediction', methods=["GET", "POST"])
def getPrediction():
    # 获取参数信息
    params = request.json
    price = params.get("price", 0)
    space = params.get("space", 0)
    region = params.get("region", "天河")
    region = region_code.get(region, -1)
    area = params.get("area", '天河大道')
    area = area_code.get(area, -1)
    living_room = params.get("living_room", 0)
    bedroom = params.get("bedroom", 0)
    predict_by_type = params.get("predict_by_type", 0)
    floor = params.get("floor", 0)
    has_elevator = bool(params.get("has_elevator", False))

    logger.info(
        f'region: {region}, predict_by_type: {predict_by_type}, has_elevator: {has_elevator}, floor: {floor}, area: {area} living_room: {living_room}, bed_room: {bedroom}, price: {price}, space: {space},')
    # 预测
    raw_response = {}
    if predict_by_type == PredictByType.PRICE.value:
        # 预测面积
        X = [area, region, floor, has_elevator, living_room, bedroom, space]
        res = space_random_forest.predict([X])[0]
    else:
        # 预期价格
        X = [area, region, floor, has_elevator, living_room, bedroom, price]
        res = price_random_forest.predict([X])[0]

    processed_res = {"prediction": res, "req": params}

    raw_response["data"] = processed_res
    response = make_response(json.dumps(raw_response, ensure_ascii=False))
    response.mimetype = 'application/json'
    return response
