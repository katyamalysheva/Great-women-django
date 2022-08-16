from women.models import *
from django.db import connection
connection.queries
from django.db.models import Min, Max, Count
def look():
    print(Women.objects.all().count())
    print(Women.objects.all()[3:8])
    Women.objects.order_by('-pk')
    Women.objects.all().reverse()
    Women.objects.filter(pk__lte=2)# less then equal 
    w = Women.objects.get(pk=2) #строго одна запись
    c3 = Category.objects.get(pk=1)
    print(c3.women_set.exists())# count() и exists() применяются к любой выборке 
    c2 = Category.objects.get(pk=2)
    print(c2.women_set.count())
    Women.objects.filter(cat__name__contains='цы')
    Category.objects.filter(women__title__contains='ли')
    Women.objects.aggregate(cat_min=Min('cat_id'), cat_max=Max('cat_id'))
    Women.objects.values('title', 'cat_id').get(pk=1) # values запрашивает не все поля
    c = Category.objects.annotate(total=Count('women')).filter(total__gt=0)
    Women.objects.raw('SELECT * FROM women_women')
    
