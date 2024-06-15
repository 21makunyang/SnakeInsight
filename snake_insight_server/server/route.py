import json
import time

from loguru import logger

from snake_insight_server.server import request, make_response, Filter
from snake_insight_server.classes import Query, Calculator
from flask import Flask, request, make_response

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
    region = params.get("region", "天河")
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
    region = params.get("region", "天河")
    require_elevator = bool(params.get("require_elevator", False))
    logger.info(region)
    raw_response = {}
    res = filter.get_floor_price(require_elevator, region)
    processed_res = {}

    for k, v in res.items():
        processed_res[k[0]] = v
        v[0] = round(v[0] * 100) / 100

    raw_response["data"] = processed_res
    raw_response["data"] = processed_res
    responce = make_response(json.dumps(raw_response, ensure_ascii=False))
    responce.mimetype = 'application/json'
    return responce