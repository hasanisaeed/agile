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
        self.sprint = Sprint.objects.filter(start__gte=datetime.datetime.now()).first()


    def get_velocity(self, user, sum_sp) -> float:
        user_sp = self.get_data(user)
        print(f'\n{user}')
        print(sum_sp)
        return float('{0:.2f}'.format(sum(user_sp) / sum_sp * 100))

    def get_context_data(self, **kwargs):
        context = super(ChartModelView, self).get_context_data(**kwargs)

        from accounts.models import CustomUser
        users = CustomUser.objects.filter(is_superuser=False).all()

        print(self.sprint)
        sum_story_point = StoryPoint.objects.filter(sprint=self.sprint).aggregate(Sum('sp'))['sp__sum']
        users_info = []
        for index, user in enumerate(users, 1):
            try:
                info = {'id': user.id,
                        'name': user.get_username(),
                        'avatar': user.avatar,
                        'color': user.color,
                        'velocity': self.get_velocity(user.id, sum_story_point)}
                users_info.append(info)
            except:
                pass

        context.update({"config": self.get_config(users_info)})
        context.update({"users": users_info})
        return context

    def get_data(self, user):
        story_point = StoryPoint.objects.filter(sprint=self.sprint, user=user).values_list('sp', flat=True)
        return list(story_point)

    def get_config(self, users):
        datasets = []
        sprint = Sprint.objects.filter(start__lte=datetime.datetime.now()).first()

        for user in users:
            data = self.get_data(user['id'])
            dataset = Dataset(label=user['name'],
                              data=data,
                              border_color=user['color'])
            datasets.append(dataset)

        chart_labels = list(StoryPoint.objects.filter(date__range=[sprint.start, sprint.end])
                            .annotate(str_date=Cast(TruncSecond('date', DateTimeField()), CharField()))
                            .values_list('str_date', flat=True))

        data = Data(labels=chart_labels, datasets=datasets)
        config = ConfigChart(data=data)

        return config.convert_to_json()
