from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Student, Feddback
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']

        #student login
        try:
            student = Student.objects.get(username=u,password=p)
            request.session['student_id']= student.id
            messages.success(request,"Student Login Successfully")
            return redirect('student_home')
            
        except Student.DoesNotExist:
            pass

        #admin login code
        admin = auth.authenticate(username=u,password=p)
        if admin is not None and admin.is_staff:
            auth.login(request,admin)
            messages.success(request,"Welcome Admin...")
            return redirect('adminhome')

    return render(request, 'login.html', {'error': error})


@login_required(login_url='login')
def adminhome(request):
    error = ""
    if request.method == 'POST':
        n= request.POST['name']
        e= request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        c= request.POST['college']
        city = request.POST['city']
        j= request.POST['join_date']
        tf= request.POST['total_fees']
        pf= request.POST['paid_fees']
        lf= request.POST['left_fees']
        p= request.POST['phone']
        t= request.POST['technology']
        image= request.FILES['image']

        try:
            Student.objects.create(name=n,email=e,username=username,password=password,college=c,city=city,join_date=j,total_fees=tf,paid_fees=pf,left_fees=lf,phone=p,technology=t,image=image)
            print("Saved Successfully")
        except:
            error="yes"
    d={"error":error}

    return render(request, 'adminhome.html', d)

@login_required(login_url='login')
def add_student(request):
    error = ""
    if request.method == "POST":
        n=request.POST['name']
        e=request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        c=request.POST['college']
        city = request.POST['city']
        jd=request.POST['join_date']
        tf=request.POST['total_fees']
        pf=request.POST['paid_fees']
        lf=request.POST['left_fees']
        ph=request.POST['phone']

        tech=request.POST['technology']
        image=request.FILES['image']
        try:
            Student.objects.create(name=n,email=e,username=username,password=password,college=c,city=city,join_date=jd,
            total_fees=tf,paid_fees=pf,left_fees=lf,phone=ph,tech=tech,image=image)
            print("saved successfully")
            error="no"
            return redirect('view_student')
        except:
            print(e)
            error="yes"
    d={"error":error}
    return render(request, 'add_student.html', d)
@login_required(login_url='login')
def view_student(request):
    data=Student.objects.all()
    d={"data":data}
    return render(request, 'view_student.html', d)

@login_required(login_url='login')
def edit_student(request,id):
    student = Student.objects.get(id=id)

    

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.username = request.POST.get("username")
        student.password = request.POST.get("password")
        student.college = request.POST.get("college")
        student.city = request.POST.get("city")
        student.join_date = request.POST.get("join_date")
        student.total_fees = request.POST.get("total_fees")
        student.paid_fees = request.POST.get("paid_fees")
        student.left_fees = request.POST.get("left_fees")
        student.phone = request.POST.get("phone")
        student.tech = request.POST.get("technology")

        if request.FILES.get("image"):
            student.image = request.FILES.get("image")

        student.save()
        return redirect('view_student')

    return render(request,'edit_student.html', {"student":student})


from django.shortcuts import get_object_or_404, redirect
from .models import Student 
@login_required(login_url='login')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("view_student")   # yahan apne view student page ka URL name likho


def search_student(request):

    if request.method == 'POST':
        n = request.POST['name']
        student= Student.objects.filter(name__icontains=n)
        d = {"student":student}
        return render(request,'search_student.html',d)
    return render(request, 'search_student.html')


def admin_logout(request):
    logout(request)
    return redirect('login')


def change_password(request):

    # Student logged in
    if 'student_id' in request.session:
        return render(request, 'change_password.html')

    # Admin logged in
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'change_password.html')

    # Koi logged in nahi hai
    return redirect('login')


def update_password(request):

    if request.method != 'POST':
        return redirect('change_password')

    old_pass = request.POST.get('old_pass')
    new_pass = request.POST.get('new_pass')
    confirm_pass = request.POST.get('confirm_pass')

    # New password aur confirm password check
    if new_pass != confirm_pass:
        messages.error(
            request,
            'New password and confirm password do not match.'
        )
        return redirect('change_password')


    # ==========================================
    # STUDENT PASSWORD CHANGE
    # ==========================================
    if 'student_id' in request.session:

        sid = request.session['student_id']

        try:
            student = Student.objects.get(id=sid)
        except Student.DoesNotExist:
            messages.error(request, 'Student not found.')
            return redirect('login')

        # Old password check
        if student.password != old_pass:
            messages.error(request, 'Old password is incorrect.')
            return redirect('change_password')

        # Update password
        student.password = new_pass
        student.save()

        # Student logout
        request.session.flush()

        messages.success(
            request,
            'Student password changed successfully. Please login again.'
        )
        return redirect('login')


    # ==========================================
    # ADMIN PASSWORD CHANGE
    # ==========================================
    elif request.user.is_authenticated and request.user.is_staff:

        user = request.user

        # Old password check
        if not user.check_password(old_pass):
            messages.error(request, 'Old password is incorrect.')
            return redirect('change_password')

        # Django hashed password update
        user.set_password(new_pass)
        user.save()

        # Admin logout
        auth.logout(request)

        messages.success(
            request,
            'Admin password changed successfully. Please login again.'
        )
        return redirect('login')


    # ==========================================
    # NOT LOGGED IN
    # ==========================================
    else:
        messages.error(request, 'Please login first.')
        return redirect('login')
    

def student_home(request):
    if 'student_id' not in request.session:
        return redirect('login')
    sid = request.session['student_id']
    student = Student.objects.get(id=sid)
    return render(request, 'student_home.html',{'student':student})


def edit_profile(request):
    if 'student_id' not in request.session:
        return redirect('login')
    sid = request.session['student_id']
    student = Student.objects.get(id=sid)

    
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.city = request.POST.get('city')
        student.phone = request.POST.get('phone')
        if request.FILES.get('image'):
            student.image = request.FILES.get('image')

        student.save()
        return redirect('student_home')
    d = {"student":student}
    return render(request,'edit_profile.html',d)


def fee_details(request):
    if 'student_id' not in request.session:
            return redirect('login')
    sid = request.session['student_id']
    student = Student.objects.get(id=sid)
    
    return render(request,'fee_details.html',{"student":student})


from django.http import HttpResponse
from reportlab.pdfgen import canvas
import datetime

def fee_receipt(request):
    sid = request.session.get('student_id')
    if sid is None:
        return redirect('login')
    student = Student.objects.get(id=sid)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="FeeReceipt.pdf"'

    pdf = canvas.Canvas(response)
    #Headings:-
    pdf.setTitle("Student Fee Receipt")
    pdf.setFont("Helvetica-Bold",22)
    pdf.drawString(140,800,"Student Record System")
    pdf.setFont("Helvetica",13)
    pdf.drawString(180,780,"STUDENT FEE RECEIPT")
    pdf.line(40,765,550,765)

    #Receipt Details:-
    receipt_no = 'SRM' + str(student.id).zfill(4)

    pdf.setFont('Helvetica-Bold',12)
    pdf.drawString(50,740,"Receipt No. : " + receipt_no)

    pdf.drawString(350,740,"Date : "+datetime.datetime.now().strftime("%d-%m-%y"))
    pdf.line(40,725,550,725)

    #Student Details:-

    pdf.setFont("Helvetica-Bold",12)
    pdf.drawString(50,700,"Student Details")
    pdf.setFont("Helvetica",13)
    pdf.drawString(50,660,"Name : " +str(student.name))
    pdf.drawString(50,645,"Email : " +str(student.email))
    pdf.drawString(50,630,"Phone : " +str(student.phone))
    pdf.drawString(50,615,"College : " +str(student.college))
    pdf.drawString(50,600,"Course : " +str(student.tech))
    pdf.line(40,545,550,545)

    #fee Details
    pdf.setFont("Helvetica-Bold",14)
    pdf.drawString(50,520,"Fee Details")
    pdf.setFont("Helvetica",12)
    pdf.drawString(50,490,"Total Fee")
    pdf.drawString(250,490,"Rs "+str(student.total_fees))
    pdf.drawString(50,465,"Paid Fee")
    pdf.drawString(250,465,"Rs "+str(student.paid_fees))
    pdf.drawString(50,440,"Remaining Fee")
    pdf.drawString(250,440,"Rs "+str(student.left_fees))

    pdf.line(40,410,550,410)

    #footer
    pdf.setFont("Helvetica",12)
    pdf.drawString(50,380,"This is Computer Generated Fee Receipt")

    pdf.setFont("Helvetica",11)
    pdf.drawString(395,140,"Authorized Signature")

    


    pdf.save()
    return response


def view_feedback(request):
    feedback = Feddback.objects.all().order_by('date')
    return render(request,"view_feedback.html",{"feedback":feedback})


def give_feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        date = request.POST['date']
        Feddback.objects.create(name=name,email=email,subject=subject,message=message,date=date)
        print('Feedback send Successfully...')


    return render(request,"give_feedback.html")