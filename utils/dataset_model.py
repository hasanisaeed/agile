import random

from django.views.generic import TemplateView

from utils.config import ConfigChart, Data, Dataset


class ChartModelView(ConfigChart, TemplateView):
    template_name = 'performance.html'

    def get_context_data(self, **kwargs):
        context = super(ChartModelView, self).get_context_data(**kwargs)
        context.update({"config": self.get_config()})
        return context

    def get_config(self):
        datasets = []
        for i in range(3):
            dataset = Dataset(label=[str(i)],
                              data=[random.randint(i, 100)])
            datasets.append(dataset)

        data = Data(labels=['A'], datasets=datasets)
        config = ConfigChart(data=data)

        return config.convert_to_json()
