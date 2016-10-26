from django.contrib import admin
from models import Country, Review
# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
	list_display=('pk','title','date','country','user')
	search_fields = ['title']
	list_filter = (
        ('country', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
    )
# class CountryAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name',)
#     list_filter = ('pk')

admin.site.register(Country)
admin.site.register(Review,ReviewAdmin)