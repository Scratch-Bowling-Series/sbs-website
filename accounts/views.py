import json
from django.template.defaulttags import register
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, send_mail

from scoreboard.ranking import get_rank_data_from_json
from tournaments.models import Tournament
from tournaments.views import get_tournament, is_valid_uuid, get_place, get_qualifying, make_ordinal
from .forms import RegisterForm, ModifyAccountForm
from .tokens import account_activation_token

User = get_user_model()


@register.filter
def counter(value, ordinal=False):
    output = ''
    try:
        value + 1
    except TypeError:
        value = 0

    for x in range(-15,2):
        if ordinal:
            if x is value:
                temp = make_ordinal(value + x)
                output += '<li>{0}</li>'.format(temp)
            else:
                temp = make_ordinal(value + x)
                output += '<li class="inactive">{0}</li>'.format(temp)
        else:
            if x is value:
                output += '<li>{0}</li>'.format(str(value + x))
            else:
                output += '<li class="inactive">{0}</li>'.format(str(value + x))
    return output


@register.filter
def none_replace(value, output):
    if value == None or value == '':
        return output
    return value


@register.filter
def is_friend(user_id, user):
    user_id = is_valid_uuid(user_id)
    if user_id != None:
        if user != None:
            friends = json.loads(user.friends)
            if str(user_id) in friends:
                return True
            else:
                return False
    return None


def accounts_modify_view(request):
    if request.method == 'POST':
        form = ModifyAccountForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            user.bio = form.data.get('bio')
            user.picture= form.cleaned_data.get('picture')
            user.location_street = form.data.get('location_street')
            user.location_city = form.data.get('location_city')
            user.location_state = form.data.get('location_state')
            zip = form.data.get('location_zip')
            if zip != None and zip != '':
                user.location_zip = zip
            right_handed = form.data.get('right_handed')
            if right_handed == 'on':
                right_handed = True
            else:
                right_handed = False
            left_handed = form.data.get('left_handed')
            if left_handed == 'on':
                left_handed = True
            else:
                left_handed = False
            user.right_handed = right_handed
            user.left_handed = left_handed
            user.finish_profile = False
            form.save()
            user.save()
            return redirect('/account/view/' + str(user.user_id))
    else:
        user = request.user
        form = ModifyAccountForm(initial={'bio': user.bio, 'location_street': user.location_street, 'location_city': user.location_city, 'location_state': user.location_state, 'location_zip': user.location_zip, 'left_handed': user.left_handed, 'right_handed': user.right_handed })
    return render(request, 'accounts/modify-account.html', {'form': form})


def accounts_login_view(request):


    email = EmailMessage(
        'Hello',
        'Body goes here',
        'no-reply@scratchbowling.pythonanywhere.com',
        ['christianjstarr@icloud.com'],
        reply_to=['christianjstarr@icloud.com'],
        headers={'Message-ID': '1'},
    )
    email.send()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form, 'result': 'CHANGED'})


# User-Auth SIGNUP
def accounts_signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(email, password)
            user.first_name = form.data['first_name']
            user.last_name = form.data.get('last_name')
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Scratch Series Bowling, Activate Account'
            email = EmailMessage(mail_subject, message, to=[email])
            email.send()
            user.save()
            return render(request, 'homepage.html', {'nbar': 'home', 'notify': 'verify_email', 'first': user.first_name})
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form':form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user !=  None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'homepage.html', {'nbar': 'home', 'notify': 'verify_email_done'})
    else:
        return render(request, 'homepage.html', {'nbar': 'home', 'notify': 'verify_email_error'})


# User-Auth LOGOUT
def accounts_logout_view(request):
    logout(request)
    return redirect('/')


# User-Auth MY Account
def accounts_account_view(request, id):
    view_user = User.objects.get(user_id=id)
    tournaments = get_recent_tournaments(view_user)
    rank_data = get_rank_data_from_json(view_user.statistics)

    return render(request, 'accounts/my-account.html', {'view_user': view_user, 'tournaments': tournaments, 'rank_data': rank_data})


def get_recent_tournaments(user):
    data = []
    if user.tournaments !=  None:
        try:
            tournaments = json.loads(user.tournaments)
        except ValueError:
            tournaments = []
        for id in tournaments:
            tournament = get_tournament(id)
            date = tournament.tournament_date
            name = tournament.tournament_name
            location = 'Linden, MI'
            place = get_place(id, user)
            uuid = str(tournament.tournament_id)

            data.append([date, name, location, place, uuid])
    return data

def update_users_tournaments():
    users = User.objects.all()
    for user in users:
        user.tournaments = None
        user.save()

    tournaments = Tournament.objects.all()
    count = 0
    for tournament in tournaments:
        count = count + 1
        uuid = str(tournament.tournament_id)
        print(tournament.tournament_name)
        qualifying = get_qualifying(tournament)
        if qualifying==None:
            continue
        for qual in qualifying:
            uu = is_valid_uuid(qual[1])
            if uu !=  None:
                bowler = User.objects.get(user_id=uu)
                b_tournaments = []
                try:
                    b_tournaments = json.loads(bowler.tournaments)
                except ValueError:
                    b_tournaments = []
                except TypeError:
                    b_tournaments = []
                b_tournaments.append(uuid)
                bowler.tournaments = json.dumps(b_tournaments)
                bowler.save()




def accounts_add_view(request, id):
    id = is_valid_uuid(id)
    if id !=  None:
        user = request.user
        if user !=  None:
            friends = []
            try:
                friends = json.loads(user.friends)
            except:
                friends = []
            if str(id) not in friends:
                friends.append(str(id))
                user.friends = json.dumps(friends)
                user.save()
    return redirect('/account/view/' + str(id))


def accounts_remove_view(request, id):
    id = is_valid_uuid(id)
    if id !=  None:
        user = request.user
        if user !=  None:
            friends = []
            try:
                friends = json.loads(user.friends)
            except:
                friends = []

            if str(id) in friends:
                friends.remove(str(id))
            user.friends = json.dumps(friends)
            user.save()
    return redirect('/account/view/' + str(id))

