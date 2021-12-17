import os
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.defaulttags import register
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ScratchBowling.sbs_utils import make_ordinal
from ScratchBowling.websettings import WebSettings
from tournaments.models import Tournament
from tournaments.views import is_valid_uuid
from .forms import RegisterForm, ModifyAccountForm
from .friends import is_friends_with, add_to_friends_list, remove_from_friends_list
from .tokens import account_activation_token
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

User = get_user_model()

# FILTERS
@register.filter
def is_friends_filter(user_id, friends_list):
    return is_friends_with(friends_list, user_id)

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




def accounts_modify_view(request):
    if request.method == 'POST':
        form = ModifyAccountForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            user.bio = form.data.get('bio')
            user.picture = form.cleaned_data.get('picture')
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
            image = Image.open('/home/scratchbowling/Scratch-Bowling-Series-Website/media/profile-pictures/' + str(user.picture))
            image = crop_max_square(image).resize((250, 250), Image.LANCZOS)
            image = image.convert('RGB')
            user.picture = 'profile-pictures/main-' + str(user.user_id) + '.jpg'
            user.save()
            image.save('/home/scratchbowling/Scratch-Bowling-Series-Website/media/profile-pictures/main-' + str(
                user.user_id) + '.jpg')
            return redirect('/account/view/' + str(user.user_id))
    else:
        user = request.user
        form = ModifyAccountForm(initial={'bio': user.bio, 'location_street': user.location_street, 'location_city': user.location_city, 'location_state': user.location_state, 'location_zip': user.location_zip, 'left_handed': user.left_handed, 'right_handed': user.right_handed })
    return render(request, 'accounts/modify-account.html', {'form': form,
                                                            'page_title': 'Modify Account',
                                                            'page_description': 'Modify your Scratch Bowling Series account.',
                                                            'page_keywords': 'Modify, Account, Edit, Change, Update, Information, Settings, Help'})

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

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

def accounts_signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(email, password)
            user.first_name = form.data['first_name']
            user.last_name = form.data.get('last_name')
            user.save()
            login(request, user)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            #mail_subject = 'Scratch Series Bowling, Activate Account'

             ##send_mail(
             ##   mail_subject,
             ##   ' ',
             ##   'christianjstarr@icloud.com',
             ##   [email],
             ##   fail_silently=True,
             ##    html_message=message
             ## )
            settings = WebSettings()
            return HttpResponseRedirect(settings.primary_domain + '/notify/verify_email/')
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

def accounts_logout_view(request):
    logout(request)
    return redirect('/')

def accounts_account_view(request, id):
    user = User.get_user_by_uuid(id)
    if user:
        statistics = user.statistics
        if statistics:
            description = 'Current Rank: ' + str(statistics.rank) + ' Attended: ' + str(statistics.attended) + ' Wins: ' + str(statistics.wins) + ' Career Avg. Score: ' + str(statistics.avg_score) + ' Career Total Games: ' + str(statistics.total_games)
        else:
            description = 'This bowler has yet to attend a tournament.'
        user_data = {'first_name': user.first_name,
                     'last_name' : user.last_name,
                     'year_joined': user.date_joined.year,
                     'city': user.location_city or '',
                     'state': user.location_state or '',
                     'handed': user.handed,
                     'picture': user.full_picture_url,
                     }

        data = {'user_data': user_data,
         'attended_tournaments': single_account_tournaments_display(user),
         'statistics': statistics.to_dict(),
         'page_title': str(user.first_name) + ' ' + str(user.last_name),
         'page_description': description,
         'page_keywords': 'user, bowler, account, rank, data, scores, tournaments, stats, statistics',
         'social_image': '/account/socialcard/image/' + str(user.user_id)
         }

        return render(request, 'accounts/my-account.html', data)
    else:
        return Http404('This user does not exist.')


def single_account_tournaments_display(user):
    tournament_ids = user.tournaments
    tournaments_data = []  ## [id, date, name, location, place]
    if tournament_ids:
        tournaments = Tournament.get_tournaments_by_uuid_list(tournament_ids)
        for tournament in tournaments:
            tournaments_data.append([tournament.tournament_id,
                                     tournament.datetime,
                                     tournament.name,
                                     tournament.center_short_location,
                                     tournament.get_place(user.user_id)])
    return tournaments_data







def accounts_socialcard_image(request, id):
    user = User.objects.filter(user_id=id).first()
    if user != None:
        pwd = os.path.dirname(__file__)
        profile_pic = Image.open('/home/scratchbowling/Scratch-Bowling-Series-Website/media/' + str(user.picture))
        profile_pic.convert('RGBA')
        profile_pic_size = (250, 250)
        profile_pic_alignment = (600 - 125, 315 - 185)
        stroke_size = 5
        stroke_color = (33, 64, 49)
        card_pic = Image.new('RGBA', (1200, 630), (255, 255, 255, 255))
        bkg = Image.open('/home/scratchbowling/Scratch-Bowling-Series-Website/assets/img/social-card-template.jpg')
        bkg.convert('RGBA')
        profile_pic = create_profile_pic_circle(profile_pic, profile_pic_size)
        profile_pic_stroke = create_profile_pic_stroke(profile_pic_size, stroke_size, stroke_color)
        card_pic.paste(bkg, (0,0))
        card_pic.paste(profile_pic, profile_pic_alignment, profile_pic)
        card_pic.paste(profile_pic_stroke,(profile_pic_alignment[0] - stroke_size, profile_pic_alignment[1] - stroke_size), profile_pic_stroke)

        fnt = ImageFont.truetype("/home/scratchbowling/Scratch-Bowling-Series-Website/assets/fonts/TTOctosquaresCond-Black.ttf", 40)
        fnt2 = ImageFont.truetype("/home/scratchbowling/Scratch-Bowling-Series-Website/assets/fonts/TTOctosquaresCond-Black.ttf", 30)
        d = ImageDraw.Draw(card_pic)

        d.text((600, 315 + 140), user.first_name + ' ' + user.last_name, font=fnt, fill=stroke_color, align="center", anchor="ms")

        d.text((600, 315 + 180), user.location_city + ', ' + user.location_state, font=fnt2, fill=stroke_color, align="center", anchor="ms")

        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = 'filename="social-card.png"'
        card_pic.save(response, "PNG")
        return response
    else:
        return Http404('This user does not exist.')

def accounts_claim_view(request, id):
    user = User.objects.filter(user_id=id).first()
    if user != None and user.unclaimed:

        if request.user.is_anonymous == False and request.user.is_authenticated:
            user.unclaimed = False
            user.save()
            request.user.location_state = user.location_state
            request.user.location_city = user.location_city
            request.user.statistics = user.statistics
            request.user.tournaments = user.tournaments
            request.user.save()
            ## Delete user
            ## Change UUID in all tournaments from user.uuid to request.user.uuid
            return HttpResponse('success')
        return HttpResponse('signed out')
    else:
        return HttpResponse('invalid user')


def create_profile_pic_stroke(profile_pic_size, stroke_size, color):

    profile_pic_size = (profile_pic_size[0] + (stroke_size * 2),
                        profile_pic_size[1] + (stroke_size * 2))
    bkg = Image.new('RGBA', profile_pic_size, (255, 255, 255, 0))
    alpha_mask = Image.new("L", profile_pic_size, 0)
    draw = ImageDraw.Draw(alpha_mask)
    draw.ellipse([(0, 0), profile_pic_size], fill=255)
    draw.ellipse([(stroke_size, stroke_size), (profile_pic_size[0] - stroke_size - 1, profile_pic_size[1] - stroke_size - 1)], fill=0)
    stroke = Image.new('RGBA', profile_pic_size, color)
    bkg.paste(stroke, (0,0), alpha_mask)
    bkg.convert('RGBA')
    return bkg

def create_profile_pic_circle(profile_pic, profile_pic_size):
    profile_pic.thumbnail(profile_pic_size)
    bkg = Image.new('RGBA', profile_pic_size, (255, 255, 255, 0))
    alpha_mask = Image.new("L", profile_pic_size, 0)
    draw = ImageDraw.Draw(alpha_mask)
    draw.ellipse([(0, 0), profile_pic_size], fill=255)

    bkg.paste(profile_pic, (0,0), alpha_mask)
    return bkg

def accounts_add_view(request, id):
    id = is_valid_uuid(id)
    if id !=  None and request.user != None:
        add_to_friends_list(request.user, id)
    return redirect('/account/view/' + str(id))

def accounts_remove_view(request, id):
    id = is_valid_uuid(id)
    if id !=  None and request.user != None:
        remove_from_friends_list(request.user, id)
    return redirect('/account/view/' + str(id))

