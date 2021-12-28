import datetime

from django.db.models import CharField, DateTimeField, Sum
from django.db.models.functions import Cast, TruncSecond

from django.views.generic import TemplateView

from accounts.models import StoryPoint, Sprint
from utils.config import ConfigChart, Data, Dataset


class ChartModelView(ConfigChart, TemplateView):
    template_name = 'performance.html'

    def __init__(self):
        super().__init__()
        self.sprint = Sprint.objects.filter(end__gte=datetime.datetime.now()).first()

    def get_velocity(self, user, sum_sp) -> float:
        user_sp = self.get_data(user)

        normalized_sp = [i / sum_sp for i in user_sp]

        return float('{0:.2f}'.format(1 - sum(normalized_sp)))

    def get_context_data(self, **kwargs):
        context = super(ChartModelView, self).get_context_data(**kwargs)

        from accounts.models import CustomUser
        users = CustomUser.objects.filter(is_superuser=False).all()

        print(self.sprint)
        sum_story_point = StoryPoint.objects.filter(sprint=self.sprint).aggregate(Sum('sp'))['sp__sum']
        users_info = []
        for index, user in enumerate(users, 1):
            info = {'id': user.id,
                    'name': user.get_username(),
                    'avatar': user.avatar,
                    'color': user.color,
                    'velocity': self.get_velocity(user.id, sum_story_point)}
            users_info.append(info)

        context.update({"config": self.get_config(users_info)})
        context.update({"users": users_info})
        return context

    def get_data(self, user):
        story_point = StoryPoint.objects.filter(sprint=self.sprint, user=user).values_list('sp', flat=True)
        return list(story_point)

    def get_chart_labels(self):
        start_date = self.sprint.start.date()
        end_date = self.sprint.end.date()

        delta = end_date - start_date

        labels = [(start_date + datetime.timedelta(days=i+1)).strftime('%Y, %d %b')
                  for i in range(delta.days )]
        return labels

    def get_config(self, users):
        datasets = []
        for user in users:
            data = self.get_data(user['id'])
            dataset = Dataset(label=user['name'],
                              data=data,
                              border_color=user['color'])
            datasets.append(dataset)

        chart_labels = self.get_chart_labels()
        data = Data(labels=chart_labels, datasets=datasets)
        config = ConfigChart(data=data)

        return config.convert_to_json()
