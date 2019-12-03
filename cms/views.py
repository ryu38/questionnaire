from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from cms.models import Question, Choice, Like, Vote
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse
from cms.form import QuestionForm, ChoiceFormset


class QuestionList(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'cms/questions.html'

    def get_queryset(self):
        return Question.objects.all().prefetch_related('choices')

    def get_context_data(self, **kwargs):
        ctx = super(QuestionList, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            voted_questions = Vote.objects.filter(user=self.request.user).values_list('question_id', flat=True)
            ctx['voted_questions'] = list(voted_questions)
        else:
            ctx['voted_questions'] = []
        return ctx


def test(request):
    queryset = list(Vote.objects.filter(user=request.user).values_list('question_id', flat=True))
    print(queryset)
    return HttpResponse('')


@login_required
def like(request, pk):
    question = get_object_or_404(Question, pk=pk)
    liking = Like.objects.filter(user=request.user).filter(question=question)
    like_check = liking.count()

    if like_check > 0:
        liking.delete()
        question.like_num -= 1
        question.save()
        messages.success(request, 'いいね！を取り消しました')
        return redirect(reverse_lazy('cms:question_list'))

    question.like_num += 1
    question.save()
    like = Like()
    like.user = request.user
    like.question = question
    like.save()
    messages.success(request, 'いいね！しました')
    return redirect(reverse_lazy('cms:question_list'))


@login_required
def vote(request, question_pk, choice_pk):
    choice = get_object_or_404(Choice, pk=choice_pk)
    choice.vote_num += 1
    choice.save()

    vote = Vote()
    vote.user = request.user
    vote.choice = choice
    vote.question = choice.question
    vote.save()

    return redirect(reverse_lazy('cms:question_list'))


def create_question(request):
    form = QuestionForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST' and form.is_valid():
        question = form.save(commit=False)
        choice_formset = ChoiceFormset(request.POST, files=request.FILES, instance=question)
        if choice_formset.is_valid():
            question.save()
            choice_formset.save()
            return redirect('cms:question_list')

        else:
            context['choice_formset'] = choice_formset

    else:
        context['choice_formset'] = ChoiceFormset()

    return render(request, 'cms/create.html', context)
