import json

from loguru import logger

from snake_insight_server.server import request, make_response
from snake_insight_server.classes import Query, Calculator


def get_info():
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
                    y_fields.append((y[0], y[1]))
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

    response = make_response(json.dumps(raw_response, ensure_ascii=False))
    response.mimetype = 'application/json'
    return response
