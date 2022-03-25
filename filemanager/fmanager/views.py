from django.shortcuts import render
import pyrebase
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.contrib import auth
from urllib.error import HTTPError

# config do podpięcia bazy danych
config = {
    'apiKey': "AIzaSyDEFfPE6-WHc59sGp0LO8fsf3uwJ8QH7Ck",
    'authDomain': "filemanager-6b90c.firebaseapp.com",
    'projectId': "filemanager-6b90c",
    'databaseURL': 'https://filemanager-6b90c-default-rtdb.europe-west1.firebasedatabase.app/',
    'storageBucket': "filemanager-6b90c.appspot.com",
    'messagingSenderId': "754019748923",
    'appId': "1:754019748923:web:8b91bf7843e5ac9ab5e01e",
    'storageBucket': 'gs://filemanager-6b90c.appspot.com'
}
# Autoryzacja bazy danych
firebase = pyrebase.initialize_app(config)
authentication = firebase.auth()
database = firebase.database()
storage = firebase.storage()


def login_page(request):
    return render(request, 'login_page.html')


def login_check(request):
    email = request.POST.get('email')
    request.session['email'] = email
    password = request.POST.get('password')
    request.session['password'] = password
    try:
        user = authentication.sign_in_with_email_and_password(email, password)
    except:
        message = "Invalid email or password"
        return render(request, 'login_page.html', {'message': message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return redirect('home_page')


def home_page(request):
    idToken = request.session['uid']
    user_id = authentication.get_account_info(idToken)
    user_id = user_id['users'][0]['localId']
    if database.child('Users').child(user_id).child('files').get().val() is not None:
        filenames = list(database.child('Users').child(user_id).child('files').shallow().get().val())
        filenames_joined = [''.join(filename.split()) for filename in filenames]
        files = database.child('Users').child(user_id).child('files').get().val()

        #Dane o pliku
        timestamps = [file['created_at'] for file in files.values()]
        url = [file['url'] for file in files.values()]
        # size = [file['size'] for file in files.values()]
        # type = [file['type'] for file in files.values()]
        comb_list = zip(filenames, timestamps, filenames_joined, url)
        return render(request, 'home_page.html', {'email': request.session['email'],
                                                  'password': request.session['password'],
                                                  'comb_list': comb_list})
    else:
        return render(request, 'home_page.html', {'email': request.session['email'],
                                                  'password': request.session['password']
                                                  })


def log_out(request):
    try:
        del request.session['uid']
        del request.session['email']
        del request.session['password']
    except KeyError:
        pass
    return render(request, 'login_page.html')

def sign_up(request):
    return render(request, 'signup_page.html')

def post_sign_up(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = authentication.create_user_with_email_and_password(email, password)
    except:
        message = "This account is already used"
        return render(request, 'signup_page.html', {'message': message})

    uid = user['localId']
    data = {'name': username, 'status': "1"}
    database.child("Users").child(uid).set(data)

    return render(request, 'login_page.html')


def add_file(request):
    return render(request, 'add_file.html')


def post_file(request):
    filename = request.POST.get('filename')
    url = request.POST.get("url")
    # size = request.POST.get("size")
    # size = int(size) / 1024
    from datetime import datetime
    created_at = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    try:
        idToken = request.session['uid']
        user_id = authentication.get_account_info(idToken)
        user_id = user_id['users'][0]['localId']
        data = {
            'created_at': created_at,
            'user_id': user_id,
            'filename': filename,
            'url':url
        }
        database.child('Users').child(user_id).child('files').child(filename).set(data, idToken)
        return redirect('home_page')

    except KeyError:
        message = "User Logged Out. Please sign in again."
        return render(request, "login_page.html", {'message': message})

def file_edit(request, filename):
    idToken = request.session['uid']
    user_id = authentication.get_account_info(idToken)
    user_id = user_id['users'][0]['localId']
    filename = database.child('Users').child(user_id).child('files').child(filename).child('filename').get().val()
    timestamp = database.child('Users').child(user_id).child('files').child(filename).child('created_at').get().val()
    username = database.child('Users').child(user_id).child('name').get().val()
    return render(request, 'file_edit.html', {'filename': filename,
                                              'timestamp': timestamp,
                                              'username': username})
