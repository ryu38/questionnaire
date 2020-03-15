from accounts.models import UserInformation


def common(request):
    if request.user.is_authenticated:
        if UserInformation.objects.filter(user=request.user).exists():
            information = UserInformation.objects.get(user=request.user)
        else:
            new_information = UserInformation()
            new_information.user = request.user
            new_information.nickname = request.user.username
            new_information.save()
            information = UserInformation.objects.get(user=request.user)
        return {'user_information': information}

    return {'user_information': 'ゲスト'}
