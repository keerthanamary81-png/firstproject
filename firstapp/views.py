from mailbox import Message
import pandas as pd
import joblib
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model,login, logout
import os
from django.conf import settings
# Create your views here.
User=get_user_model()

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login

User = get_user_model()

def login_func(request):
    tes = 'welcome To Login Page'

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user_check = authenticate(
            request,
            username=username,
            password=password
        )

        if user_check is not None:
            login(request, user_check)
            return redirect('homepage_view')

        else:
            error_message = 'Invalid username or password'
            return render(
                request,
                'login.html',
                {
                    'tes': tes,
                    'error_message': error_message
                }
            )

    # GET request handle
    return render(request, 'login.html', {'tes': tes})

def register_func(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_val=User(username=username)
        user_val.set_password(password)
        user_val.save()
        return redirect('login_func')
    else:
        Message='welcome to register'
        return render(request,'register.html',{'reg':Message})
    
def homepage_view(request):
    if not request.user.is_authenticated:
        return redirect('login_func')
    return render(request,'home.html')

def logout_user(request):
    logout(request)
    return redirect('login_func')

import pandas as pd
from django.shortcuts import render, redirect


def predict_page(request):

    if not request.user.is_authenticated:
        return redirect('login_func')

    if request.method == 'POST':

        # =========================
        # LOAD CSV
        # =========================

        csv_path = os.path.join(settings.BASE_DIR, 'Housing.csv')

        df = pd.read_csv(csv_path)

        # lowercase conversion
        string_cols = [

            "mainroad",
            "guestroom",
            "basement",
            "hotwaterheating",
            "airconditioning",
            "prefarea",
            "furnishingstatus"

        ]

        for col in string_cols:

            df[col] = df[col].astype(str).str.lower()

        # =========================
        # USER INPUT
        # =========================

        area = int(request.POST.get('area'))
        bedrooms = int(request.POST.get('bedrooms'))
        bathrooms = int(request.POST.get('bathrooms'))
        stories = int(request.POST.get('stories'))
        parking = int(request.POST.get('parking'))

        mainroad = request.POST.get('mainroad').lower()
        guestroom = request.POST.get('guestroom').lower()
        basement = request.POST.get('basement').lower()
        hotwaterheating = request.POST.get('hotwaterheating').lower()
        airconditioning = request.POST.get('airconditioning').lower()
        prefarea = request.POST.get('prefarea').lower()
        furnishingstatus = request.POST.get('furnishingstatus').lower()

        # =========================
        # FILTER DATA
        # =========================

        result = df[

            (df['area'] == area) &
            (df['bedrooms'] == bedrooms) &
            (df['bathrooms'] == bathrooms) &
            (df['stories'] == stories) &
            (df['parking'] == parking) &
            (df['mainroad'] == mainroad) &
            (df['guestroom'] == guestroom) &
            (df['basement'] == basement) &
            (df['hotwaterheating'] == hotwaterheating) &
            (df['airconditioning'] == airconditioning) &
            (df['prefarea'] == prefarea) &
            (df['furnishingstatus'] == furnishingstatus)

        ]

        # =========================
        # CHECK RESULT
        # =========================

        if not result.empty:

            price = result.iloc[0]['price']

            return render(

                request,
                'predict.html',
                {
                    'prediction': price
                }

            )

        else:

            return render(

                request,
                'predict.html',
                {
                    'prediction': 'No Exact Match Found'
                }

            )

    return render(request, 'predict.html')