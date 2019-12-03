from django.contrib import admin
from cms.models import Question, Choice, Like, Vote


# Register your models here.
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'choice', 'vote_num')
    list_display_links = ('id', 'choice')
    raw_id_fields = ('question', )


admin.site.register(Choice, ChoiceAdmin)


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('id', 'text', )
    list_display_links = ('id', 'text', )


admin.site.register(Question, QuestionAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question')


admin.site.register(Like, LikeAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'choice')


admin.site.register(Vote, VoteAdmin)
