import csv

from django.http import HttpRequest, HttpResponse
from django.db.models.options import Options
from django.db.models.query import QuerySet


class Export_goods_mixin():
    def export_csv(self, request: HttpRequest, queryset: QuerySet ):
        meta: Options = self.models._meta
        fields_name = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content_Disposition'] = f'attachment; filename={meta}-export.csv'

        csv_writer = csv.writer(response)

        csv.writer.writerow(fields_name)

        for row in queryset:
            csv_writer.writerow([getattr(row, field) for fields in fields_name])

        return response

    export_csv.short_description = 'Выгрузка в csv файл'