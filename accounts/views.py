from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from accounts.models import UserInformation, UserImage
from accounts.form import UserInformationForm, UserImageForm
from cms.models import Question, Vote, Choice
from cms.form import QuestionForm, ChoiceFormset
import datetime
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


# POST TempleteView NG
@login_required
def information(request):
    ctx = {}

    # プロフィール
    if UserInformation.objects.filter(user=request.user).exists():
        ctx['information'] = UserInformation.objects.get(user=request.user)
    else:
        new_information = UserInformation()
        new_information.user = request.user
        new_information.nickname = request.user.username
        new_information.save()
        ctx['information'] = UserInformation.objects.get(user=request.user)

    image = UserImage.objects.filter(user=request.user).last()
    form = UserImageForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        if not image:
            image = form.save(commit=False)
            image.user = request.user
        else:
            image.image = request.FILES['image']
        image.save()
        image = UserImage.objects.filter(user=request.user).last()
    else:
        form = UserImageForm()
    ctx['image_form'] = form
    ctx['image'] = image

    # 自分の質問
    questions = Question.objects.filter(user=request.user, expired=False)

    deadline_date = list(questions.values_list('deadline', flat=True))
    for i, question in enumerate(questions):
        if deadline_date[i] <= timezone.now():
            question.expired = True
            question.save()

    display_questions = \
        Question.objects.filter(user=request.user).prefetch_related('choices').order_by('expired', '-date_created')[:6]

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

    votes = Vote.objects.filter(user=request.user)
    ctx['voted_questions'] = list(votes.values_list('question_id', flat=True))
    ctx['voted_choices'] = list(votes.values_list('choice_id', flat=True))

    ctx['form'] = QuestionForm()
    ctx['choice_formset'] = ChoiceFormset()

    return render(request, 'accounts/account.html', ctx)


@login_required
def edit_information(request):
    information = get_object_or_404(UserInformation, user=request.user)
    form = UserInformationForm(request.POST)
    print(form)
    if form.is_valid():
        information.nickname = form.cleaned_data['nickname']
        sex = request.POST.get('sex')
        if sex == '---':
            sex = None
        information.sex = sex
        information.age = form.cleaned_data['age']

        secret_list = [request.POST.get('age_secret'), request.POST.get('sex_secret')]
        for i, check in enumerate(secret_list):
            if check is not None:
                secret_list[i] = 1
            else:
                secret_list[i] = 0
        if sum(secret_list) == 0:
            information.secret = 'none'
        else:
            print(secret_list)
            str_list = [str(n) for n in secret_list]
            information.secret = '/'.join(str_list)

        information.save()

        if request.POST.get('delete_image') and UserImage.objects.filter(user=request.user).exists():
            image = UserImage.objects.filter(user=request.user).last()
            image.delete()

        return redirect('accounts:account')

    form = UserInformationForm()
    ctx = {'form': form, 'information': information}
    return render(request, 'accounts/edit_information.html', ctx)


def add_question(request):
    c = int(request.GET.get('loaded_count'))
    str_displayed_questions_pk = request.GET.get('displayed')
    if str_displayed_questions_pk:
        displayed_questions_pk = str_displayed_questions_pk.split('/')
        print(str_displayed_questions_pk)
    else:
        displayed_questions_pk = [0]

    additional_questions = \
        Question.objects.filter(user=request.user).exclude(pk__in=displayed_questions_pk).order_by('expired', '-date_created')[:6]
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

        votes = Vote.objects.filter(user=request.user)
        voted_questions = list(votes.values_list('question_id', flat=True))
        voted_choice_pks = list(votes.values_list('choice_id', flat=True))

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
