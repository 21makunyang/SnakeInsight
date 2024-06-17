from typing import *

from snake_insight_server.classes import Query


class StatisticalMethod(object):
    def __init__(self, *, return_tuple=False):
        self.return_tuple = return_tuple
        pass

    def add(self, _id, value) -> None:
        pass

    def result(self) -> Any:
        pass

    def clear(self) -> None:
        pass


class Max(StatisticalMethod):
    def __init__(self, *, return_tuple=False):
        super().__init__(return_tuple=return_tuple)
        self.max: dict[str | int | float, float] = {}

    def add(self, _id, value):
        self.max[_id] = self.max.get(_id, value)
        if value > self.max[_id]:
            self.max[_id] = value

    def result_tuple(self):
        result = []
        for k, v in self.max.items():
            result.append((k, v))
        result.sort(key=lambda item: item[0])
        return result

    def result(self):
        if self.return_tuple:
            return self.result_tuple()
        return self.max

    def clear(self):
        self.max = {}


class Min(StatisticalMethod):
    def __init__(self, *, return_tuple=False):
        super().__init__(return_tuple=return_tuple)
        self.min: dict[str | int | float, float] = {}

    def add(self, _id, value):
        self.min[_id] = self.min.get(_id, value)
        if value < self.min[_id]:
            self.min[_id] = value

    def result_tuple(self):
        result = []
        for k, v in self.min.items():
            result.append((k, v))
        result.sort(key=lambda item: item[0])
        return result

    def result(self):
        if self.return_tuple:
            return self.result_tuple()
        return self.min

    def clear(self):
        self.min = {}


class Avg(StatisticalMethod):
    def __init__(self, *, return_tuple=False):
        super().__init__(return_tuple=return_tuple)
        self.avg: dict[str, tuple[float, int]] = {}

    def add(self, _id, value):
        _v, _c = self.avg.get(_id, (0, 0))
        self.avg[_id] = (_v + value, _c + 1)

    def result_tuple(self):
        result = []
        for k, v in self.avg.items():
            s, n = v
            result.append((k, round(s / n * 100) / 100 if n != 0 else 0.0))
        result.sort(key=lambda item: item[0])
        return result

    def result(self):
        if self.return_tuple:
            return self.result_tuple()
        result = {}
        for k, v in self.avg.items():
            s, n = v
            result[k] = round(s / n * 100) / 100 if n != 0 else 0.0
        return result

    def clear(self):
        self.avg = {}

class Count(StatisticalMethod):
    def __init__(self, *, return_tuple=False):
        super().__init__(return_tuple=return_tuple)
        self.count: dict[str | int | float, int] = {}

    def add(self, _id, value):
        self.count[_id] = self.count.get(_id, 0) + 1

    def result_tuple(self):
        result = []
        for k, v in self.count.items():
            result.append((k, v))
        result.sort(key=lambda item: item[0])
        return result

    def result(self):
        if self.return_tuple:
            return self.result_tuple()
        return self.count

    def clear(self):
        self.count = {}


class Box(StatisticalMethod):
    def __init__(self, *, return_tuple=False):
        super().__init__()
        self.box: dict[str | int | float, tuple[Avg, list[int | float]]] = {}

    def Q(self, _id, index: int):
        """
        返回一组数据的四分位数
        :param _id:
        :param index: 第几四分位数(1 <= index <= 3)
        :return:
        """
        avg, data = self.box.get(_id, (Avg(), []))
        i_Q = len(data) * index // 4
        return data[i_Q]

    def IQR(self, _id):
        return self.Q(_id, 3) - self.Q(_id, 1)

    def MID(self, _id):
        _, data = self.box.get(_id, (Avg(), []))
        return data[len(data) // 2]

    def add(self, _id, value):
        self.box[_id] = self.box.get(_id, (Avg(), []))
        self.box[_id][0].add(_id, value)
        self.box[_id][1].append(value)
        self.box[_id][1].sort()

    def result(self):
        result = {}
        for k, v in self.box.items():
            # 分别代表[下边缘, 下四分位数, 中位数, 上四分位数, 上边缘]
            r = [self.Q(k, 1) - 1.5 * self.IQR(k),
                 self.Q(k, 1),
                 self.MID(k),
                 self.Q(k, 3),
                 self.Q(k, 3) + 1.5 * self.IQR(k)]

            lower_outer_limit = self.Q(k, 1) - 3.0 * self.IQR(k)  # 下外限
            lower_inner_limit = self.Q(k, 1) - 1.5 * self.IQR(k)  # 下内限
            upper_inner_limit = self.Q(k, 3) + 1.5 * self.IQR(k)  # 上内限
            upper_outer_limit = self.Q(k, 1) + 3.0 * self.IQR(k)  # 上外限

            mild_outliers = []
            extreme_outliers = []

            avg, data = self.box[k]
            for value in data:
                if lower_inner_limit <= value <= upper_inner_limit:
                    continue
                elif lower_outer_limit <= value < lower_inner_limit or upper_inner_limit < value <= upper_outer_limit:
                    mild_outliers.append(value)
                else:
                    extreme_outliers.append(value)
            result[k] = (r, mild_outliers, extreme_outliers)
        return result

    def clear(self):
        self.box = {}


class Raw(StatisticalMethod):
    def __init__(self, *, return_tuple=False):
        super().__init__(return_tuple=return_tuple)
        self.raw: dict[str | int | float, list] = {}

    def add(self, _id, value):
        self.raw[_id] = self.raw.get(_id, [])
        self.raw[_id].append(value)

    def result_tuple(self):
        result = []
        for k, v in self.raw.items():
            result.append((k, v))
        result.sort(key=lambda item: item[0])
        return result

    def result(self):
        if self.return_tuple:
            return self.result_tuple()
        else:
            return self.raw

    def clear(self):
        self.raw = {}


ProcessOptions: dict[str, StatisticalMethod.__class__] = {"Max": Max, "Min": Min, "Avg": Avg, "Count": Count, "Box": Box, "Raw": Raw}


class Calculator(object):
    def __init__(self, query: Query, *, x_field: str | tuple, y_fields: list[tuple[str, str, bool]]):
        self.query = query
        self.x = x_field
        self.ys = y_fields

    def plot_data(self, detailed_data: bool = False) -> dict | list:
        __operators: dict[tuple[str, str], StatisticalMethod] = {}
        for y in self.ys:
            field_name, operator, return_tuple = y
            if operator not in ProcessOptions:
                raise ValueError(f"Unexpected operator({operator})")
            __operators[(field_name, operator)] = ProcessOptions[operator](return_tuple=return_tuple)
        for _dict in self.query.fetch(exclude_field=["raw", "unit", "community"], auto_convert=True):
            for __op_id, __op in __operators.items():
                __field_name, _ = __op_id
                if isinstance(self.x, str):
                    __op.add(_dict[self.x], _dict[__field_name])
                else:
                    try:
                        __xs = []
                        for __x in self.x:
                            __xs.append(_dict[__x])
                        __op.add(tuple(__xs), _dict[__field_name])
                    except Exception as e:
                        raise TypeError(f"Unexpected error({e}) at {__file__}.")

        if detailed_data:
            __plot_data = []
            for __op_id, __op in __operators.items():
                __field_name, __method = __op_id
                __result = __op.result()
                __detail = {"x_field": self.x,
                            "y_field": __field_name,
                            "return_tuple": __op.return_tuple,
                            "method": __method,
                            "value": __result}
                __plot_data.append(__detail)
        else:
            __plot_data = {}
            for __op_id, __op in __operators.items():
                identifier = "_".join(__op_id)
                __plot_data[identifier] = __op.result()

        return __plot_data
