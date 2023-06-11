from django.contrib import admin

from .models import Question, Choice

# Basic registration of your models here.
# admin.site.register(Question)
# admin.site.register(Choice)

#Customizing the admin form to control how it looks and works

# Reorders the page so pub date is at the top
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text'] 

# Separates into sections on the django admin page, and formats it neatly
class ChoiceInline(admin.StackedInline): #admin.TabularInline will make it a tablex
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date'],
        'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]



admin.site.register(Question, QuestionAdmin)