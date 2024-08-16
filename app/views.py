from django.shortcuts import render, HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from .forms import AddUserForm, RemoveUserForm, EditUserForm 
from .models import Level, Question, Subject
from django.db.models import Count
import random


def register_view(request):
    if request.method == "POST":
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return redirect('/register')

        if len(password) < 8:
            messages.warning(request, "Password must be at least 8 characters long")
            return redirect('/register')

        try:
            if User.objects.get(username=uname):
                messages.info(request, "Username already exists")
                return redirect('/register')
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=email):
                messages.info(request, "Email already exists")
                return redirect('/register')
        except User.DoesNotExist:
            pass

        muser = User.objects.create_user(username=uname, email=email, password=password)
        user.save()
        messages.success(request, "Signup successful")
        return redirect('/login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('login')

# def manage_users(request):
#     users = User.objects.all()
#     return render(request, 'quiz_users.html', {'users': users})


def quiz_users(request):
    users = User.objects.all()
    return render(request, 'quiz_users.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'True'
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = is_staff
        user.save()

        messages.success(request, 'User added successfully!')
        return redirect('manage_users')

    return render(request, 'add_user.html')

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        is_staff = request.POST.get('is_staff') == 'True'
        
        user.username = username
        user.email = email
        user.is_staff = is_staff
        user.save()

        messages.success(request, 'User updated successfully!')
        return redirect('manage_users')

    return render(request, 'update_user.html', {'user': user})

@require_POST
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('manage_users')



# For managing levels
def manage_levels(request):
    levels = Level.objects.all()
    return render(request, 'manage_levels.html', {'levels': levels})

def add_level(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        difficulty = request.POST.get('difficulty')

        if not name:
            messages.error(request, 'Level name is required.')
            return redirect('add_level')
        
        level = Level.objects.create(name=name, difficulty=difficulty)
        messages.success(request, 'Level added successfully!')
        return redirect('manage_levels')

    return render(request, 'add_level.html')



def update_level(request, level_id):
    level = get_object_or_404(Level, id=level_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        difficulty = request.POST.get('difficulty')
        
        level.name = name
        level.difficulty = difficulty
        level.save()

        messages.success(request, 'Level updated successfully!')
        return redirect('manage_levels')

    return render(request, 'update_level.html', {'level': level})

def delete_level(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    if request.method == 'POST':
        level.delete()
        messages.success(request, 'Level deleted successfully!')
        return redirect('manage_levels')
    return render(request, 'delete_level.html', {'level': level})



# For managing subjects
def manage_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'manage_subjects.html', {'subjects': subjects})


def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon')
        description = request.POST.get('description')
        if not all([name, icon, description]):
            messages.error(request, 'All field is required.')
            return redirect('add_subject')
        
        subjects = Subject.objects.create(name=name, icon=icon, description=description)
        messages.success(request, 'Subject added successfully!')
        return redirect('manage_subjects')

    return render(request, 'add_subject.html')


def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon')
        description = request.POST.get('description')
        
        subject.name = name
        subject.icon = icon
        subject.description = description
        subject.save()

        messages.success(request, 'Subject updated successfully!')
        return redirect('manage_subjects')

    return render(request, 'update_subject.html', {'subject': subject})


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('manage_subjects')

    return render(request, 'manage_subjects.html', {'object': subject})




# For managing questions
def manage_questions(request):
    questions = Question.objects.all()
    return render(request, 'manage_questions.html', {'questions': questions})

def add_question(request):
    if request.method == 'POST':
        level_id = request.POST.get('level')
        question_text = request.POST.get('question_text')
        correct_answer = request.POST.get('correct_answer')
        option_1 = request.POST.get('option_1')
        option_2 = request.POST.get('option_2')
        option_3 = request.POST.get('option_3')
        option_4 = request.POST.get('option_4')

        if not all([question_text, correct_answer, option_1, option_2, option_3, option_4]):
            messages.error(request, 'All fields are required.')
            return redirect('add_question')

        level = get_object_or_404(Level, id=level_id)
        subject = get_object_or_404(Subject, id=subject_id)
        Question.objects.create(
            subject=subject,
            level=level,
            question_text=question_text,
            correct_answer=correct_answer,
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4
        )
        messages.success(request, 'Question added successfully!')
        return redirect('manage_questions')

    subjects = Subject.objects.all()
    levels = Level.objects.all()
    return render(request, 'add_question.html', {'levels': levels, 'subjects': subjects})

def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        correct_answer = request.POST.get('correct_answer')
        option_1 = request.POST.get('option_1')
        option_2 = request.POST.get('option_2')
        option_3 = request.POST.get('option_3')
        option_4 = request.POST.get('option_4')

        if not all([question_text, correct_answer, option_1, option_2, option_3, option_4]):
            messages.error(request, 'All fields are required.')
            return redirect('update_question', question_id=question.id)

        question.question_text = question_text
        question.correct_answer = correct_answer
        question.option_1 = option_1
        question.option_2 = option_2
        question.option_3 = option_3
        question.option_4 = option_4
        question.save()

        messages.success(request, 'Question updated successfully!')
        return redirect('manage_questions')

    return render(request, 'update_question.html', {'question': question})

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('manage_questions')

    return render(request, 'confirm_delete.html', {'object': question})





def index(request):
    
    subjects = Subject.objects.all()
    return render(request,'index.html', {'subjects': subjects})

def about(request):
    return render(request,'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if not all([name, email, message]):
            messages.error(request, 'All fields are required.')
            return redirect('contact')

        

    return render(request, 'contact.html')

def history(request):
    return render(request,'history.html')

def leaderboard(request):
    return render(request,'leaderboard.html')


def game_level(request, subject_name):
    subject = get_object_or_404(Subject, name=subject_name)
    levels = Level.objects.all()
    return render(request, 'game_level.html', {'subject': subject, 'levels': levels})


def game_start(request, subject_name, level_name):
    subject = Subject.objects.get(name=subject_name)
    level = Level.objects.get(name=level_name)
    
    if request.method == 'POST':
        # Fetch 10 random questions from the database
        questions = Question.objects.filter(subject=subject, level=level).order_by('?')[:10]
        if not questions.exists():
            return render(request, 'game_start.html', {'subject': subject, 'level': level, 'questions': questions, 'no_questions': True})

        return render(request, 'game_start.html', {'subject': subject, 'level': level, 'questions': questions, 'no_questions': False})

    return render(request, 'game_start.html', {'subject': subject, 'level': level})


def submit_quiz(request, subject_name, level_name):
    if request.method == 'POST':
        score = 0
        total_questions = 10

        # Get all questions for the selected subject and level
        questions = Question.objects.filter(subject__name=subject_name, level__name=level_name)

        for question in questions:
            # total_questions += 1
            selected_answer = request.POST.get(f'question_{question.id}')

            if selected_answer == question.correct_answer:  # Assuming you have a correct_answer field in your Question model
                score += 1

        # Calculate the percentage score
        percentage_score = (score / total_questions) * 100

        # Provide feedback to the user
        messages.success(request, f'You scored {score} out of {total_questions} ({percentage_score:.2f}%).')

        return redirect('game_level', subject_name=subject_name)

    return redirect('game_level', subject_name=subject_name)
