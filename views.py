from django.shortcuts import render, redirect
from .forms import RegisterForm, PatientForm
from .models import PatientRecord
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import joblib
import numpy as np
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Load the trained model and label encoders
model = joblib.load('cirrhosis_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def predict_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)

            input_data = {
                'N_Days': patient.n_days,
                'Status': patient.status,
                'Drug': patient.drug,
                'Age': patient.age,
                'Sex': patient.sex,
                'Ascites': patient.ascites,
                'Hepatomegaly': patient.hepatomegaly,
                'Spiders': patient.spiders,
                'Edema': patient.edema,
                'Bilirubin': patient.bilirubin,
                'Cholesterol': patient.cholesterol,
                'Albumin': patient.albumin,
                'Copper': patient.copper,
                'Alk_Phos': patient.alk_phos,
                'SGOT': patient.sgot,
                'Tryglicerides': patient.triglycerides,
                'Platelets': patient.platelets,
                'Prothrombin': patient.prothrombin,
            }

            # Encode categorical fields
            for col in ['Status', 'Drug', 'Sex', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema']:
                input_data[col] = label_encoders[col].transform([input_data[col]])[0]

            # Predict
            features = np.array([list(input_data.values())])
            stage = model.predict(features)[0]

            # Convert NumPy int64 to native int
            stage = int(stage)

            # Save patient
            patient.stage = stage
            patient.user = request.user
            patient.save()

            # Save to session (now JSON serializable)
            request.session['stage'] = stage

            return redirect('result')
    else:
        form = PatientForm()

    return render(request, 'predict.html', {'form': form})

@login_required
@login_required
def result_view(request):
    stage = request.session.get('stage', None)

    if stage is None:
        return redirect('predict')

    # Descriptions and recommendations for liver disease stages
    stage_info = {
        1: {
            'description': 'Early fibrosis – liver still functions well.',
            'recommendation': 'Adopt a healthy diet, avoid alcohol, and monitor liver function regularly.'
        },
        2: {
            'description': 'Moderate fibrosis – damage progressing.',
            'recommendation': 'Strict lifestyle control, medication adherence, and regular follow-ups are essential.'
        },
        3: {
            'description': 'Severe fibrosis (pre-cirrhosis) – liver structure is distorted.',
            'recommendation': 'Close monitoring by a hepatologist and possible need for intervention.'
        },
        4: {
            'description': 'Cirrhosis – significant liver damage.',
            'recommendation': 'Regular ultrasounds, liver function tests, possible transplant evaluation.'
        }
    }

    # Safely get info
    info = stage_info.get(stage, {
        'description': 'Unknown stage.',
        'recommendation': 'Please consult a specialist for accurate guidance.'
    })

    # Pass all to template
    return render(request, 'result.html', {
        'stage': stage,
        'description': info['description'],
        'recommendation': info['recommendation']
    })

@login_required
def history_view(request):
    records = PatientRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, 'history.html', {'records': records})
