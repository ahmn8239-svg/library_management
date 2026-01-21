from django import forms
from .models import Book, Author, Category, Member, Employee, Borrow
from django.contrib.auth.models import User

# ==========================================
# BOOKS FORMS
# ==========================================

class BookForm(forms.ModelForm):
  
    author_names = forms.CharField(
        label='المؤلفين', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل أسماء المؤلفين مفصولة بفاصلة'}),
        help_text='افصل بين الأسماء بفاصلة (،)'
    )
    category_name = forms.CharField(
        label='التصنيف', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم التصنيف'}),
        required=True
    )

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'publication_year', 'total_copies', 'available_copies', 'cover_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            
            authors = self.instance.authors.all()
            self.fields['author_names'].initial = "، ".join([a.name for a in authors])
           
            if self.instance.category:
                self.fields['category_name'].initial = self.instance.category.name

    def save(self, commit=True):
        
        book = super(BookForm, self).save(commit=False)
        
       
        cat_name = self.cleaned_data['category_name'].strip()
        if cat_name:
            category, created = Category.objects.get_or_create(name=cat_name)
            book.category = category
        
        if commit:
            book.save()
            self.save_m2m()
           
            author_names_str = self.cleaned_data['author_names']
           
            names = [name.strip() for name in author_names_str.replace(',', '،').split('،') if name.strip()]
            
            new_authors = []
            for name in names:
                author, created = Author.objects.get_or_create(name=name)
                new_authors.append(author)
            
           
            book.authors.set(new_authors)
            
        return book

# ==========================================
# MEMBERS FORMS
# ==========================================

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['user', 'full_name', 'email', 'phone', 'membership_type', 'membership_level', 'max_borrow_limit']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'membership_type': forms.Select(attrs={'class': 'form-control'}),
            'membership_level': forms.Select(attrs={'class': 'form-control'}),
            'max_borrow_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# ==========================================
# EMPLOYEES FORMS
# ==========================================

class EmployeeForm(forms.ModelForm):
    
    username = forms.CharField(label='اسم المستخدم', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المستخدم'}))
    email = forms.EmailField(label='البريد الإلكتروني', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}))
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    confirm_password = forms.CharField(label='تأكيد كلمة المرور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    first_name = forms.CharField(label='الاسم الأول', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الأول'}))
    last_name = forms.CharField(label='اسم العائلة', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم العائلة'}))

    class Meta:
        model = Employee
        fields = ['role', 'phone', 'address']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '05xxxxxxxx'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'العنوان بالتفصيل'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('اسم المستخدم هذا مستخدم بالفعل.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('البريد الإلكتروني هذا مستخدم بالفعل.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "كلمتا المرور غير متطابقتين")


class EmployeeUpdateForm(forms.ModelForm):
   
    new_password = forms.CharField(required=False, label='كلمة مرور جديدة', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'اتركه فارغاً إذا كنت لا تريد تغييره'}))
    confirm_password = forms.CharField(required=False, label='تأكيد كلمة المرور الجديدة', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))

    class Meta:
        model = Employee
        fields = ['role', 'phone', 'address']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "كلمتا المرور غير متطابقتين")
        return cleaned_data

# ==========================================
# BORROWING FORMS
# ==========================================

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['book', 'member', 'employee', 'due_date', 'return_date', 'status']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'member': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
