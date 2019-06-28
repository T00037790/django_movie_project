from django.db.models import QuerySet, Sum, Count, FloatField


class UserQueryset(QuerySet):
    def get_by_year(self, username=None):
        if username:
            return self.filter(user=username)
        else:
            return self


class MovieRateQueryset(QuerySet):
    def get_best_rated(self):
        return self.values('movie').annotate(
            rate=Sum('rate') / Count('movie', output_field=FloatField())).order_by('-rate')
