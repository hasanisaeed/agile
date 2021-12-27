from django.db.models import ForeignObject
from django.db.models.options import Options
from django.db.models.sql.datastructures import Join
from django.db.models.sql.where import ExtraWhere


def join_to(table1, table2, field1, field2, queryset, alias=''):
    """
    table1 base
    """

    # here you can set complex clause for join
    def extra_join_cond(where_class, _alias, related_alias):
        if (_alias, related_alias) == ('[sys].[columns]',
                                       '[sys].[database_permissions]'):
            where = '[sys].[columns].[column_id] = ' \
                    '[sys].[database_permissions].[minor_id]'
            children = [ExtraWhere([where], ())]
            wh = where_class(children)
            return wh
        return None

    dpj = ForeignObject(
        to=table2,
        on_delete=lambda: None,
        from_fields=[None],
        to_fields=[None],
        rel=None,
        related_name=None
    )
    dpj.opts = Options(table1._meta)
    dpj.opts.model = table1
    dpj.get_joining_columns = lambda: ((field1, field2),)
    dpj.get_extra_restriction = extra_join_cond

    dj = Join(
        table2._meta.db_table, table1._meta.db_table,
        'T', "LEFT JOIN", dpj, True)

    ac = queryset._clone()
    print(ac.query)
    ac.query.join(dj)
    alias and setattr(dj, 'table_alias', alias)
    return ac
