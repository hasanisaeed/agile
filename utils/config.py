import json


class ConfigChart:
    def __init__(self, chart_type='bar', data=None, options=None):
        self.chart_type = chart_type
        self.data = data
        self.options = options

    def chart_type(self):
        return self.chart_type

    def data(self):
        return self.data

    def options(self):
        return self.options

    def repr_json(self):
        return dict(type=self.chart_type,
                    data=self.data,
                    # options=self.options
                    )

    def convert_to_json(self):
        _json = json.dumps(self.repr_json(), cls=ComplexEncoder)
        return json.loads(_json)


class Data:
    def __init__(self, labels=None, datasets=None):
        self.labels = labels
        self.datasets = datasets

    def labels(self):
        return self.labels

    def datasets(self):
        return self.datasets

    def repr_json(self):
        return dict(labels=self.labels,
                    datasets=self.datasets)


class Dataset:
    def __init__(self, label='', data=0, border_color='#000', bg_color='#fe9100'):
        self.label = [label]
        self.data = [data]
        self.border_color = border_color
        self.background_color = bg_color

    def label(self):
        return self.label

    def data(self):
        return self.data

    def border_color(self):
        return self.border_color

    def background_color(self):
        return self.background_color

    def repr_json(self):
        return dict(label=self.label,
                    data=self.data,
                    borderColor=self.border_color,
                    backgroundColor=self.background_color
                    )


class ComplexEncoder(json.JSONEncoder):
    """Recursive convert class type to json object."""

    def default(self, obj):
        if hasattr(obj, 'repr_json'):
            return obj.repr_json()
        else:
            return json.JSONEncoder.default(self, obj)
