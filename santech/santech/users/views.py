from django.shortcuts import render, redirect
from django.contrib.auth import  login, logout
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render
from .expert_system import MedicalExpertSystem 
from .models import Data
from threading import Thread
from .mqtt import start_mqtt_consumer
from django.http import JsonResponse

# Page d'accueil
def index(request):
    return render(request, 'users/index.html')

# Page about
def about(request):
    return render(request, 'users/about.html')

# Page contact
def contact(request):
    return render(request, 'users/contact.html')

# Page service
def service(request):
    return render(request, 'users/service.html')

# Page appointment
def appointment(request):
    return render(request, 'users/appointment.html')

# Page feature
def feature(request):
    return render(request, 'users/feature.html')

# Page team
def team(request):
    return render(request, 'users/team.html')

# Page testimonial
def testimonial(request):
    return render(request, 'users/testimonial.html')
# Page 404
def page_not_found(request):
    return render(request, '404.html')

# Page de connexion
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('diagnostic')
        else:
            messages.error(request, "Error during registration. Please check your information.")
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")    
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Page d'inscription
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, "Error during registration. Please check your information.")
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")

    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Page de réinitialisation du mot de passe
def forgot_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='users/password_reset_email.html',
                subject_template_name='users/password_reset_subject.txt',
                from_email=None,
            )
            messages.success(request, "A password reset link has been sent to your email.")
            return render(request, 'users/forgot_password.html', {'form': form})
        else:
            messages.error(request, "Please enter a valid email address.")
    else:
        form = PasswordResetForm()

    return render(request, 'users/forgot_password.html', {'form': form})
# Page de déconnexion
def logout_view(request):
    logout(request)
    return redirect('index')


def latest_data_api(request):
    last_data = Data.objects.filter(temperature__isnull=False, bpm__isnull=False).order_by('-timestamp').first()
    if last_data:
        return JsonResponse({
            'temperature': last_data.temperature,
            'bpm': last_data.bpm,
            'oxygene': last_data.oxygene,
            'timestamp': last_data.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return JsonResponse({'error': 'Aucune donnée disponible'}, status=404)

def diagnostic_view(request):
    start_mqtt_thread()
    last_data = Data.objects.filter(temperature__isnull=False, bpm__isnull=False).order_by('-timestamp').first()

    resultats = []
    recommendations = []
    error = None
    temperature = None
    heart_rate = None
    oxygene = None

    if last_data:
        temperature = last_data.temperature
        heart_rate = last_data.bpm
        oxygene = last_data.oxygene  
        expert_system = MedicalExpertSystem()

        try:
            resultats, recommendations = expert_system.analyser_symptomes(temperature, heart_rate, oxygene)
        except Exception as e:
            error = f"Erreur lors du diagnostic automatique : {e}"
    context = {
        'data': last_data,  
        'temperature': temperature,
        'temperature': temperature,
        'oxygene': oxygene,
        'resultats': resultats,
        'recommendations': recommendations,
        'error': error,
    }
    return render(request, 'users/diagnostic.html', context)


def start_mqtt_thread():
    mqtt_thread = Thread(target=start_mqtt_consumer)
    mqtt_thread.daemon = True
    mqtt_thread.start()
