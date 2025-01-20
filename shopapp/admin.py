from django.contrib import admin
from django.http import HttpRequest
from django.db.models.query import QuerySet

from .admin_mixins import Export_goods_mixin
# Register your models here.

from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description='Безопасное удаление')
def mark_archived(modedladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Восстановление')
def mark_unarchived(modedladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, Export_goods_mixin):


    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]

    inlines = [
        OrderInline,
    ]

    list_display = 'pk','name','description_short','price','discount', 'archived'
    list_display_links = 'pk','name'
    ordering = ['-pk']
    search_fields = 'name','description'

    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Настройка цены', {
            'fields': ('price', 'discount'),
            'classes': ('collapse',),
        }),
        ('Дополнительные опции', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Безопасное удаление'
        }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + '...'


class ProductInline(admin.TabularInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    inlines = [
        ProductInline,
    ]

    list_display = 'pk', 'adress', 'promo', 'created_at','user'
    list_display_links = 'pk', 'adress'

    def get_queryset(self, request):
        return Order.objects.select_related('user')


    #def user_name(self, obj: Order) -> str:
        #return obj.user.firs_name or obj.user.username


#admin.site.register(Product, ProductAdmin)