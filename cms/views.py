from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from cms.models import Question, Choice, Like, Vote
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from cms.form import QuestionForm, ChoiceFormset
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
import datetime
from django.utils import timezone
from accounts.models import UserImage, UserInformation
from django.db.models import Q
from django.template.context_processors import csrf
import pdb

User = get_user_model()


# class OnlyYouMixin(UserPassesTestMixin):
#     raise_exception = True
#
#     def test_func(self):
#         user = self.request.user
#         return user.pk == self.kwargs['user_pk'] or user.is_superuser


class QuestionList(TemplateView):
    template_name = 'cms/questions.html'

    def get_context_data(self, **kwargs):
        ctx = super(QuestionList, self).get_context_data(**kwargs)
        questions = Question.objects.filter(expired=False)

        if self.request.user.is_authenticated:
            votes = Vote.objects.filter(user=self.request.user)
            ctx['voted_questions'] = list(votes.values_list('question_id', flat=True))
            ctx['voted_choices'] = list(votes.values_list('choice_id', flat=True))
        else:
            ctx['voted_questions'] = []
            ctx['voted_choices'] = []

        deadline_date = list(questions.values_list('deadline', flat=True))
        for i, question in enumerate(questions):
            if deadline_date[i] <= timezone.now():
                question.expired = True
                question.save()

        keyword = self.request.GET.get('query')
        filtering = self.request.GET.get('filter')

        if filtering == 'voted':
            filter_question = ctx['voted_questions']
            display_questions = Question.objects.filter(pk__in=filter_question).order_by('-date_created').prefetch_related('choices')[:6]

        elif keyword:
            choice_contain = Choice.objects.filter(choice__icontains=keyword).values_list('question_id', flat=True)
            display_questions = Question.objects.filter(
                Q(text__icontains=keyword) | Q(pk__in=choice_contain)).order_by('-date_created').prefetch_related('choices')[:6]

        else:
            display_questions = Question.objects.filter(expired=False).exclude(
                pk__in=ctx['voted_questions']).order_by('deadline').prefetch_related('choices')[:6]

        deadline_date = list(display_questions.values_list('deadline', flat=True))
        deadlines = []
        localdeadlines = []
        for deadline in deadline_date:
            local_deadline = localtime(deadline)
            deadlines.append(deadline.strftime('%Y/%m/%d %H:%M:%S'))
            localdeadlines.append(local_deadline.strftime('%Y/%m/%d %H:%M:%S'))
        dates_lists = [deadlines, localdeadlines]

        ctx['deadlines'] = dates_lists[0]
        ctx['local_deadlines'] = dates_lists[1]

        total = []
        for question in display_questions:
            votes_num_list = list(Choice.objects.filter(question=question).values_list('vote_num', flat=True))
            total.append(sum(votes_num_list))

        ctx['questions'] = zip(display_questions, total)

        ctx['form'] = QuestionForm()
        ctx['choice_formset'] = ChoiceFormset()

        return ctx


def create(request):
    form = QuestionForm(request.POST)
    if form.is_valid():
        question = form.save(commit=False)
        choice_formset = ChoiceFormset(request.POST, instance=question)
        print(question)

        if choice_formset.is_valid():
            question.user = request.user
            day = int(request.POST.get('day'))
            hour = int(request.POST.get('hour'))
            minute = int(request.POST.get('minute'))
            question.deadline = timezone.now() + timezone.timedelta(days=day, hours=hour, minutes=minute)
            if request.POST.get('hide_name') is not None:
                question.hide_name = True
            question.save()
            choice_formset.save()
            ctx = {
                'created': 1,
                'problem': 0
            }
            return JsonResponse(ctx)

        else:
            problem = 'choice'
    else:
        problem = 'question'

    ctx = {
        'created': 0,
        'problem': problem
    }

    return JsonResponse(ctx)


def delete_question(request):
    question_id = request.POST.get('question_id')
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    ctx = {'deleted_question': question_id}
    return JsonResponse(ctx)


def add_question(request):
    c = int(request.GET.get('loaded_count'))
    str_displayed_questions_pk = request.GET.get('displayed')
    keyword = request.GET.get('keyword')
    filtering = request.GET.get('filter')
    if str_displayed_questions_pk:
        displayed_questions_pk = str_displayed_questions_pk.split('/')
        print(str_displayed_questions_pk)
    else:
        displayed_questions_pk = [0]

    if request.user.is_authenticated:
        votes = Vote.objects.filter(user=request.user)
        voted_questions = list(votes.values_list('question_id', flat=True))
    else:
        voted_questions = []


    if filtering == 'voted':
        filter_question = voted_questions
        additional_questions = Question.objects.filter(pk__in=filter_question).exclude(pk__in=displayed_questions_pk).order_by('-date_created').prefetch_related(
            'choices')[:6]

    elif keyword:
        choice_contain = Choice.objects.filter(choice__icontains=keyword).values_list('question_id', flat=True)
        additional_questions = Question.objects.filter(
            Q(text__icontains=keyword) | Q(pk__in=choice_contain)).exclude(pk__in=displayed_questions_pk).order_by('-date_created').prefetch_related(
            'choices')[:6]

    else:
        displayed_questions_pk.extend(voted_questions)
        additional_questions = Question.objects.filter(expired=False).exclude(
            pk__in=displayed_questions_pk).order_by('deadline').prefetch_related('choices')[:6]

    if additional_questions.count():
        pk_list = []
        text_list = []
        deadline_list = []
        local_deadline_list = []
        total_list = []
        user_list = []
        image_list = []

        choices_list = []
        choice_pks_list = []
        rates_list = []
        for question in additional_questions:
            pk_list.append(question.pk)
            text_list.append(question.text)
            deadline = question.deadline
            local_deadline = localtime(deadline)
            deadline_list.append(deadline.strftime('%Y/%m/%d %H:%M:%S'))
            local_deadline_list.append(local_deadline.strftime('%Y/%m/%d %H:%M:%S'))
            if not question.hide_name:
                user_information = UserInformation.objects.get(user=question.user)
                user_list.append(user_information.nickname)
                try:
                    image = UserImage.objects.get(user=question.user)
                except UserImage.DoesNotExist:
                    image_list.append(0)
                else:
                    image_list.append(image.image.url)
            else:
                user_list.append('hidden')
                image_list.append(0)

            choices = Choice.objects.filter(question=question)
            choices_list.append(list(choices.values_list('choice', flat=True)))
            choice_pks_list.append(list(choices.values_list('pk', flat=True)))
            votes_num_list = list(choices.values_list('vote_num', flat=True))
            total = sum(votes_num_list)
            total_list.append(total)
            rate_list = []
            if total:
                for i in votes_num_list:
                    result = round(i*100 / total)
                    rate_list.append(result)
            else:
                for i in votes_num_list:
                    rate_list.append(0)
            rates_list.append(rate_list)

        if request.user.is_authenticated:
            votes = Vote.objects.filter(user=request.user)
            voted_questions = list(votes.values_list('question_id', flat=True))
            voted_choice_pks = list(votes.values_list('choice_id', flat=True))
        else:
            voted_questions = []
            voted_choice_pks = []

        voted_check = []
        for question in pk_list:
            if question in voted_questions:
                voted_check.append(0)
            else:
                voted_check.append(1)

        ctx = {
            'question_pk_list': pk_list,
            'text_list': text_list,
            'deadline_list': deadline_list,
            'local_deadline_list': local_deadline_list,
            'user_list': user_list,
            'image_list': image_list,
            'total_list': total_list,
            'choices_list': choices_list,
            'choice_pks_list': choice_pks_list,
            'rates_list': rates_list,
            'voted_check': voted_check,
            'voted_choice_pks': voted_choice_pks,
            'not_zero': 1,
        }

    else:
        ctx = {
            'not_zero': 0
        }

    return JsonResponse(ctx)


def vote(request):
    choice_pk = request.GET.get('choice_pk')
    question_pk = request.GET.get('question_pk')

    choice = get_object_or_404(Choice, pk=choice_pk)
    choice.vote_num += 1
    choice.save()

    if request.user.is_authenticated:
        vote = Vote()
        vote.user = request.user
        vote.choice = choice
        vote.question = choice.question
        vote.save()

    choices = Choice.objects.filter(question__pk=question_pk)
    votes_num_list = list(choices.values_list('vote_num', flat=True))
    total = sum(votes_num_list)

    rates_list = []
    for i in votes_num_list:
        result = round(i*100 / total)
        rates_list.append(result)

    ctx = {
        'rates_list': rates_list,
        'total_num': total
    }

    if not request.user.is_authenticated:
        choice = get_object_or_404(Choice, pk=choice_pk)
        choice.vote_num -= 1
        choice.save()

    return JsonResponse(ctx)


class UsersQuestionList(TemplateView):
    template_name = 'cms/users_questions.html'

    def get_context_data(self, **kwargs):
        ctx = super(UsersQuestionList, self).get_context_data(**kwargs)
        questions = Question.objects.filter(user=self.request.user)

        if self.request.user.is_authenticated:
            votes = Vote.objects.filter(user=self.request.user)
            ctx['voted_questions'] = list(votes.values_list('question_id', flat=True))
            ctx['voted_choices'] = list(votes.values_list('choice_id', flat=True))
        else:
            ctx['voted_questions'] = []
            ctx['voted_choices'] = []

        voted_dates = list(questions.values_list('date_created', flat=True))
        remain_time = datetime.timedelta(days=1)
        localdates = []
        strfdates = []
        localdeadlines = []
        deadlines = []
        for date in voted_dates:
            local_date = localtime(date)
            strfdates.append(date.strftime('%Y/%m/%d %H:%M:%S'))
            localdates.append(local_date.strftime('%Y/%m/%d %H:%M:%S'))
            deadline = date + remain_time
            deadlines.append(deadline.strftime('%Y/%m/%d %H:%M:%S'))
            localdeadline = localtime(deadline)
            localdeadlines.append(localdeadline.strftime('%Y/%m/%d %H:%M:%S'))
        ctx['local_dates'] = localdates
        ctx['voted_dates'] = strfdates
        ctx['deadlines'] = deadlines
        ctx['local_deadlines'] = localdeadlines

        total = []

        for i, question in enumerate(questions):
            if voted_dates[i] + remain_time <= timezone.now():
                question.expired = True
                question.save()

            votes_num_list = list(Choice.objects.filter(question=question).values_list('vote_num', flat=True))
            total.append(sum(votes_num_list))

        display_questions = questions.prefetch_related('choices')
        ctx['questions'] = zip(display_questions, total)

        return ctx


# 以下未使用
# def test(request): テスト用
#     queryset = list(Vote.objects.filter(user=request.user).values_list('question_id', flat=True))
#     print(queryset)
#     return HttpResponse('')


# @login_required
# def like(request, pk):　いいね機能
#     question = get_object_or_404(Question, pk=pk)
#     liking = Like.objects.filter(user=request.user).filter(question=question)
#     like_check = liking.count()
#
#     if like_check > 0:
#         liking.delete()
#         question.like_num -= 1
#         question.save()
#         messages.success(request, 'いいね！を取り消しました')
#         return redirect(reverse_lazy('cms:question_list'))
#
#     question.like_num += 1
#     question.save()
#     like = Like()
#     like.user = request.user
#     like.question = question
#     like.save()
#     messages.success(request, 'いいね！しました')
#     return redirect(reverse_lazy('cms:question_list'))


# class LikedList(LoginRequiredMixin, ListView):　いいねリスト
#     model = Like
#     context_object_name = 'favorites'
#     template_name = 'cms/favorite.html'
#
#     def get_queryset(self):
#         return Like.objects.all().select_related()
#
#     def get_context_data(self, **kwargs):
#         ctx = super(LikedList, self).get_context_data(**kwargs)
#         if self.request.user.is_authenticated:
#             voted_questions = Vote.objects.filter(user=self.request.user).values_list('question_id', flat=True)
#             ctx['voted_questions'] = list(voted_questions)
#         else:
#             ctx['voted_questions'] = []
#
#         return ctx
