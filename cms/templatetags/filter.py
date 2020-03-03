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


@register.filter(name='votes_rate')
def votes_rate(vote_num, total):
    result = round(vote_num*100 / total)
    # result = '{:.0%}'.format(vote_num / total)
    # result = str(vote_num) + '/' + str(total)
    return result


@register.filter(name='your_vote')
def your_vote(choice_id, voted_choices):
    if choice_id in voted_choices:
        return True
    else:
        return False
