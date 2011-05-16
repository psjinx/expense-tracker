from django.contrib import admin
from main.models import *

class ProjectInline(admin.TabularInline):

    model = Project
    extra = 2

class OrganisationAdmin(admin.ModelAdmin):

    fieldsets = [
                (None,   {
                            'fields': ['title', 'users'],
                         }
                ),
    ]
    #readonly_fields = (,)
    filter_horizontal = ('users',)
    list_display = ('title', 'id')
    list_filter = ['title']
    search_fields = ['title']
    inlines = [ProjectInline]
    #date_hierarchy = 'time'

class LocationAdmin(admin.ModelAdmin):

    fieldsets = [
            (None, {
                'fields':['title'],
            })
    ]

    #readonly_fields = (,)
    #filter_horizontal = (,)
    list_display = ('title', 'id')
    list_filter = ['title']
    search_fields = ['title']
    #date_hierarchy = 'time'

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
            (None, {
                'fields':['title'],
            })
    ]

    #readonly_fields = (,)
    #filter_horizontal = (,)
    list_display = ('title', 'id')
    list_filter = ['title']
    search_fields = ['title']
    #date_hierarchy = 'time'

class ExpenseAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ExpenseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(type='Official', 
                         token__organisation__in=request.user.organisation_set.all())

    fieldsets = [
            (None, {
                'fields':['user' , 'organisation', 'type', 'amount', 'location',
                          'time', 'add_time'],
            }),
            ('Meta', {
                'fields': ['project', 'category', 'billed', 'bill_id', 'bill_image'],
            },)
    ]

    readonly_fields = ('user', 'organisation', 'add_time')
    #filter_horizontal = (,)
    list_display = ('user', 'organisation', 'amount', 'type', 'location', 
                    'time')
    list_filter = ['token__user__username', 'token__organisation__title',
                   'location', 'category', 'project']
    list_select_related = True
    search_fields = ['token__user__username', 'token__organisation__title',
                     'location__title', 'category__title', 'project__title']
    date_hierarchy = 'time'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Expense, ExpenseAdmin)
