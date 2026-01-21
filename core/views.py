from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Author, Category, Member, Employee, Borrow
from .forms import BookForm, MemberForm, EmployeeForm, EmployeeUpdateForm, BorrowForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# ==========================================
# DASHBOARD / HOME VIEW
# ==========================================

@login_required
def home(request):
    context = {
        'total_books': Book.objects.count(),
        'total_members': Member.objects.count(),
        'total_employees': Employee.objects.count(),
        'total_borrowed': Borrow.objects.filter(status='active').count(),
        'latest_books': Book.objects.order_by('-id')[:5],
        'latest_borrowings': Borrow.objects.order_by('-borrow_date')[:5],
    }
    return render(request, 'index.html', context)

def is_manager_or_admin(user):
    return user.is_superuser or (hasattr(user, 'employee') and user.employee.role == 'manager')

# ==========================================
# ==========================================
# BOOKS VIEWS
# ==========================================

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'title': 'إضافة كتاب جديد'})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('core:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'title': 'تعديل بيانات الكتاب'})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('core:book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book, 'title': book.title})

# ==========================================
# MEMBERS VIEWS
# ==========================================

@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'members/member_detail.html', {'member': member, 'title': member.full_name})

@login_required
def member_list(request):
    members = Member.objects.all()
    return render(request, 'members/member_list.html', {'members': members})

@login_required
def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:member_list')
    else:
        form = MemberForm()
    return render(request, 'members/member_form.html', {'form': form, 'title': 'إضافة عضو جديد'})

@login_required
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('core:member_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/member_form.html', {'form': form, 'title': 'تعديل بيانات العضو'})

@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('core:member_list')
    return render(request, 'members/member_confirm_delete.html', {'member': member})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# ==========================================
# EMPLOYEES VIEWS
# ==========================================

@login_required
@user_passes_test(is_manager_or_admin)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee, 'title': employee.user.get_full_name() or employee.user.username})

@login_required
@user_passes_test(is_manager_or_admin)
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def is_manager_or_admin(user): 
    return user.is_superuser or (hasattr(user, 'employee') and user.employee.role == 'manager')

@login_required
@user_passes_test(is_manager_or_admin)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
           
            employee = form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect('core:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'إضافة موظف جديد (إنشاء حساب)'})

@login_required
@user_passes_test(is_manager_or_admin)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user = employee.user
                user.set_password(new_password)
                user.save()
            return redirect('core:employee_list')
    else:
        form = EmployeeUpdateForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'تعديل بيانات الموظف'})

@login_required
@user_passes_test(is_manager_or_admin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
         
        user = employee.user
        employee.delete()
        user.delete()
        return redirect('core:employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

# ==========================================
# BORROWING VIEWS
# ==========================================

@login_required
def borrowing_detail(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    return render(request, 'borrowing/borrow_detail.html', {'borrow': borrow, 'title': 'تفاصيل الإعارة'})

@login_required
def borrowing_list(request):
    borrowings = Borrow.objects.all()
    return render(request, 'borrowing/borrow_list.html', {'borrowings': borrowings})

@login_required
def borrowing_create(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:borrowing_list')
    else:
        form = BorrowForm()
    return render(request, 'borrowing/borrow_form.html', {'form': form, 'title': 'تسجيل إعارة جديدة'})

@login_required
def borrowing_update(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    if request.method == 'POST':
        form = BorrowForm(request.POST, instance=borrow)
        if form.is_valid():
            form.save()
            return redirect('core:borrowing_list')
    else:
        form = BorrowForm(instance=borrow)
    return render(request, 'borrowing/borrow_form.html', {'form': form, 'title': 'تعديل بيانات الإعارة'})

@login_required
def borrowing_delete(request, pk):
    borrow = get_object_or_404(Borrow, pk=pk)
    if request.method == 'POST':
        borrow.delete()
        return redirect('core:borrowing_list')
    return render(request, 'borrowing/borrow_confirm_delete.html', {'borrow': borrow})


import logging
# استدعاء الـ logger الذي عرفناه في settings
security_logger = logging.getLogger('security_logger')

@login_required
@user_passes_test(is_manager_or_admin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        user_name = employee.user.username
        admin_user = request.user.username # الشخص الذي قام بالحذف
        
        # تسجيل العملية أمنياً قبل الحذف
        security_logger.info(f"تنبيه أمني: قام المستخدم {admin_user} بحذف حساب الموظف {user_name}")
        
        user = employee.user
        employee.delete()
        user.delete()
        return redirect('core:employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})