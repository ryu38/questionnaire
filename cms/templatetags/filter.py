from django import template
from cms.models import Vote
from cms.views import QuestionList

register = template.Library()


@register.filter(name='votes_check')
def votes_check(question_id, voted_questions):
    if question_id in voted_questions:
        return False
    else:
        return True
