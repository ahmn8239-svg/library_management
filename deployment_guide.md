# دليل رفع مشروع Django إلى الإنترنت (PythonAnywhere)

لهذا المشروع، سنستخدم منصة **PythonAnywhere** لأنها سهلة الاستخدام ومناسبة جداً لمشاريع Django.

## الخطوات الأساسية:

### 1. تجهيز الكود (لقد قمت بذلك بالفعل في المشروع):
- إعداد ملف `requirements.txt` بجميع المكتبات المطلوبة.
- إعداد ملف `.env` للمفاتيح السرية.
- إعداد `whitenoise` للتعامل مع الملفات الثابتة (CSS, JS).

### 2. رفع الكود إلى GitHub (اختياري ولكنه مفضل):
- قم بإنشاء مستودع (Repository) جديد على GitHub.
- قم برفع ملفات المشروع إليه.

### 3. إعداد الحساب على PythonAnywhere:
1. قم بإنشاء حساب مجاني على [PythonAnywhere](https://www.pythonanywhere.com/).
2. افتح "Console" جديد بنوع **Bash**.
3. قم بسحب مشروعك من GitHub:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```
   أو قم برفع الملفات يدوياً إذا لم تستخدم GitHub.

### 4. إنشاء بيئة افتراضية (Virtual Environment):
داخل الـ Bash Console:
```bash
mkvirtualenv --python=/usr/bin/python3.10 myvenv  # استبدل 3.10 بنسخة بايثون الخاصة بك
pip install -r requirements.txt
```

### 5. إعداد قاعدة البيانات والملفات الثابتة:
```bash
python manage.py migrate
python manage.py collectstatic
```

### 6. إعداد Web App على PythonAnywhere:
1. اذهب إلى تبويب **Web**.
2. اضغط على **Add a new web app**.
3. اختر **Manual Configuration** (مهم جداً).
4. اختر نسخة البايثون (مثلاً 3.10).
5. في إعدادات التطبيق:
   - **Source code**: مسار مجلد المشروع (مثلاً `/home/username/library_management`).
   - **Working directory**: نفس المسار السابق.
   - **Virtualenv**: مسار البيئة الافتراضية (مثلاً `/home/username/.virtualenvs/myvenv`).
   - **WSGI configuration file**: اضغط لتعديله وتأكد من ربط Django بشكل صحيح (سأوضح الكود الخاص به أدناه).

### 7. إعداد الملفات الثابتة (Static Files):
في أسفل صفحة Web:
- **URL**: `/static/` -> **Directory**: مسار `staticfiles` داخل مشروعك.
- **URL**: `/media/` -> **Directory**: مسار `media` داخل مشروعك.

---

> [!TIP]
> سأقوم الآن بتحديث ملف `settings.py` ليكون جاهزاً للعمل مباشرة في البيئة السحابية.
