import json
import os

from PIL import Image, ImageDraw
from django.http import HttpRequest, HttpResponse, Http404, FileResponse
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
from .scraper import UpdateUsers
from .tokens import account_activation_token
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

User = get_user_model()


@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.is_online = True
    user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.is_online = False
    user.save()

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
    return render(request, 'accounts/modify-account.html', {'form': form,
                                                            'page_title': 'Modify Account',
                                                            'page_description': 'Modify your Scratch Bowling Series account.',
                                                            'page_keywords': 'Modify, Account, Edit, Change, Update, Information, Settings, Help'})


def accounts_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form,
                                                   'result': 'CHANGED',
                                                   'page_title': 'Log In',
                                                   'page_description': 'Log into your Scratch Bowling Series account.',
                                                   'page_keywords': 'Login, Log In, Account, User, Add, Signup',
                                                   })


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
            user.save()
            send_mail(
                mail_subject,
                ' ',
                'christianjstarr@icloud.com',
                [email],
                fail_silently=True,
                html_message=message
            )
            return render(request, 'homepage.html', {'nbar': 'home', 'notify': 'verify_email', 'first': user.first_name})
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form':form,
                                                    'page_title': 'Sign Up',
                                                    'page_description': 'Create your Scratch Bowling Series account.',
                                                    'page_keywords': 'Sign Up, Create, Account, Login, Log In',
                                                    })


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
    view_user = User.objects.filter(user_id=id).first()
    if view_user != None:
        tournaments = get_recent_tournaments(view_user)
        rank_data = get_rank_data_from_json(view_user.statistics)
        if rank_data != None:
            description = 'Current Rank: ' + str(make_ordinal(rank_data.rank)) + ' Attended: ' + str(rank_data.attended) + ' Wins: ' + str(rank_data.wins) + ' Career Avg. Score: ' + str(rank_data.avg_score_career) + ' Career Total Games: ' + str(rank_data.total_games_career)
        else:
            description = 'This bowler has yet to attend a tournament.'
        return render(request, 'accounts/my-account.html', {'view_user': view_user,
                                                            'tournaments': tournaments,
                                                            'rank_data': rank_data,
                                                            'tournaments_length': len(tournaments),
                                                            'page_title': str(view_user.first_name) + ' ' + str(view_user.last_name),
                                                            'page_description': description,
                                                            'page_keywords': 'user, bowler, account, rank, data, scores, tournaments, stats, statistics',
                                                            'social_image' : '/account/socialcard/image/' + str(view_user.user_id)
                                                            })
    else:
        return Http404('This user does not exist.')


def accounts_socialcard_image(request, id):
    user = User.objects.filter(user_id=id).first()
    if user != None:
        pwd = os.path.dirname(__file__)
        profile_pic = Image.open('/home/scratchbowling/Scratch-Bowling-Series-Website/media/' + str(user.picture))
        profile_pic_size = (250, 250)
        card_pic = Image.open('/home/scratchbowling/Scratch-Bowling-Series-Website/assets/img/social-card-template.png')
        profile_pic = create_profile_pic_circle(profile_pic, profile_pic_size)
        card_pic.paste(profile_pic, (0, 0), profile_pic)
        response = HttpResponse(content_type='image/jpg')
        response['Content-Disposition'] = 'filename="social-card.png"'
        card_pic.save(response, "PNG")
        return response
    else:
        return Http404('This user does not exist.')


def create_profile_pic_circle(profile_pic, profile_pic_size):
    profile_pic.thumbnail(profile_pic_size)
    alpha_mask = Image.new("L", profile_pic_size, 0)
    draw = ImageDraw.Draw(alpha_mask)
    draw.ellipse([(0, 0), profile_pic_size], fill=255)
    profile_pic.putalpha(alpha_mask)
    return profile_pic



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


def accounts_scraper_view(request):
    data = UpdateUsers()
    return HttpResponse(str(data))



def get_amount_online():
    return User.objects.filter(is_online=True).count()


