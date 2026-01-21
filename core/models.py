from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import timedelta, date

# ==========================================
# BOOKS MODELS
# ==========================================

class Category(models.Model):
    name = models.CharField(_('اسم التصنيف'), max_length=100)
    
    class Meta:
        db_table = 'books_category'
        verbose_name = _('تصنيف')
        verbose_name_plural = _('التصنيفات')
        
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(_('اسم المؤلف'), max_length=200)
    biography = models.TextField(_('السيرة الذاتية'), blank=True)
    
    class Meta:
        db_table = 'books_author'
        verbose_name = _('مؤلف')
        verbose_name_plural = _('المؤلفين')
        
    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', _('متاح')),
        ('borrowed', _('مستعار')),
        ('reserved', _('محجوز')),
        ('lost', _('مفقود')),
    ]
    
    title = models.CharField(_('عنوان الكتاب'), max_length=200)
    isbn = models.CharField(_('الرقم التسلسلي (ISBN)'), max_length=13, unique=True)
    authors = models.ManyToManyField(Author, verbose_name=_('المؤلفين'), related_name='books', db_table='books_book_authors')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_('التصنيف'))
    publication_year = models.PositiveIntegerField(_('سنة النشر'), null=True, blank=True)
    total_copies = models.PositiveIntegerField(_('عدد النسخ الكلي'), default=1)
    available_copies = models.PositiveIntegerField(_('النسخ المتاحة'), default=1)
    cover_image = models.ImageField(_('صورة الغلاف'), upload_to='books/covers/', blank=True, null=True)
    status = models.CharField(_('الحالة'), max_length=20, choices=STATUS_CHOICES, default='available')
    added_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'books_book'
        verbose_name = _('كتاب')
        verbose_name_plural = _('الكتب')
        
    def __str__(self):
        return self.title

# ==========================================
# MEMBERS MODELS
# ==========================================

class Member(models.Model):
    MEMBERSHIP_TYPES = [
        ('student', _('طالب')),
        ('teacher', _('معلم')),
        ('visitor', _('زائر')),
    ]
    
    MEMBERSHIP_LEVELS = [
        ('regular', _('عادي')),
        ('silver', _('فضي')),
        ('gold', _('ذهبي')),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('المستخدم (حساب الدخول)'))
    full_name = models.CharField(_('الاسم الكامل'), max_length=200)
    email = models.EmailField(_('البريد الإلكتروني'), blank=True)
    phone = models.CharField(_('رقم الهاتف'), max_length=20)
    membership_type = models.CharField(_('نوع العضوية'), max_length=20, choices=MEMBERSHIP_TYPES, default='student')
    membership_level = models.CharField(_('مستوى العضوية'), max_length=20, choices=MEMBERSHIP_LEVELS, default='regular')
    max_borrow_limit = models.PositiveIntegerField(_('الحد الأقصى للإعارة'), default=3)
    current_borrowed = models.PositiveIntegerField(_('الكتب المستعارة حالياً'), default=0)
    
    class Meta:
        db_table = 'members_member'
        verbose_name = _('عضو')
        verbose_name_plural = _('الأعضاء')
        
    def __str__(self):
        return self.full_name


# ==========================================
# EMPLOYEES MODELS
# ==========================================

class Employee(models.Model):
    ROLES = [
        ('manager', _('مدير')),
        ('librarian', _('أمين مكتبة')),
        ('assistant', _('مساعد')),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('المستخدم (حساب الدخول)'))
    role = models.CharField(_('الدور الوظيفي'), max_length=20, choices=ROLES, default='librarian')
    phone = models.CharField(_('رقم الهاتف'), max_length=20)
    address = models.TextField(_('العنوان'), blank=True)
    
    class Meta:
        db_table = 'employees_employee'
        verbose_name = _('موظف')
        verbose_name_plural = _('الموظفين')
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"

# ==========================================
# BORROWING MODELS
# ==========================================

class Borrow(models.Model):
    STATUS_CHOICES = [
        ('active', _('نشط')),
        ('returned', _('تم الإرجاع')),
        ('overdue', _('متأخر')),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('الكتاب'))
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name=_('العضو'))
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, verbose_name=_('الموظف المسؤول'))
    borrow_date = models.DateField(_('تاريخ الإعارة'), auto_now_add=True)
    due_date = models.DateField(_('تاريخ الاستحقاق'), null=True, blank=True)
    return_date = models.DateField(_('تاريخ الإرجاع'), null=True, blank=True)
    fine_amount = models.DecimalField(_('قيمة الغرامة'), max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(_('الحالة'), max_length=20, choices=STATUS_CHOICES, default='active')
    
    class Meta:
        db_table = 'borrowing_borrow'
        verbose_name = _('سجل إعارة')
        verbose_name_plural = _('سجلات الإعارة')
        
    def save(self, *args, **kwargs):
        if not self.due_date:
            start_date = self.borrow_date if self.borrow_date else date.today()
            self.due_date = start_date + timedelta(days=14) 
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.book.title} - {self.member.full_name}"
