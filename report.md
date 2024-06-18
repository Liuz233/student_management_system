# 学籍管理系统设计报告

# 前期设计

### 需求分析

计划实现一个学籍管理系统

##### 数据需求

* 学生信息：包括学号、姓名、入学时间、专业、奖惩情况

其中学号是定长字符串

姓名是变长字符串

入学时间是日期类型的字符串

专业是变长字符串

奖惩情况是int类型整数，代表奖励次数-受惩罚次数



* 选课信息：包括学生学号、课程号、成绩

成绩是一个0-100的整数



* 课程信息：包括课程号、课程名、授课教师、开课年份、学分

课程号是定长字符串

课程名是变长字符串

授课教师是变长字符串

开课年份是一个日期类型的字符串

学分是一个整数



##### 功能需求

1.可以在前端增加学生信息

2.可以在前端增加课程信息

3.可以在前端增加选课信息，要求学生和课程均已存在

4.可以修改学生课程成绩

5.可以修改学生专业

6.可以修改学生奖惩信息

7.可以查询GPA

8.具有管理员系统和学生系统，权限不同。

9.可以执行登录注册功能

### 概念设计：ER图

![](./src/ER图.png)

### 逻辑设计

设计关系模式如下

1.学生(<u>学号</u>，姓名，入学时间，专业，奖惩情况)

2.课程(<u>课程号</u>，课程名，授课教师，开课年份，学分)

3.选课表(<u>学号</u>，<u>课程号</u>，成绩)

以上关系模式的设计符合3NF

## 实现说明

此项目已经上传到[github仓库](https://github.com/Liuz233/student_management_system.git)

### 框架结构

项目大体框架如下

```
myproject/
├── admin_system/ /# 管理员系统
│   ├── migrations/
│   ├── templates/   # 存放所有html文件
│   │   └── ....
|   ├── static/ # 存放使用的css文件和背景图片等
│   │   ├── css/
│   │   └── images/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py # 存放和数据库中表相对应的模型
│   ├── tests.py 
│   ├── urls.py # 存放url到视图函数的映射
│   └── views.py # 存放后端写的视图函数
├── stu_system/ /# 学生系统，与管理员系统结构类似
│   └── ....
├── djangoProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py # 主页面以及主页面到各个app的映射
│   └── wsgi.py
├── report.md # 课题设计报告
├── src/ # 图片存储
├── source/ # 触发器、存储过程、函数及其它sql代码
├── manage.py # 系统启动以及其他功能
```

其中`admin_system`实现的功能和结构如下

```
登录功能
主页
	学生管理
		编辑学生信息
		删除学生信息
		添加学生信息
	课程管理
		编辑课程信息
		删除课程信息
		添加课程信息
	选课管理
		修改学生成绩
		添加学生选课记录
		删除学生选课记录
```

`stu_system`实现的功能和结构如下

```
登录功能
注册功能（只有学生学号信息在数据库中，才能注册）
主页-已选课程和成绩
	退课
	选课
	个人信息
		上传图片
		查看总gpa
```

### 核心代码解析

由于代码量比较大，选用`admin_system`中的添加选课功能为例，讲解整个系统代码逻辑

`urls.py`路由配置

```python
from django.urls import path

from . import views
urlpatterns = [
    path('',views.toLogin),
    path('index/', views.login),
    path('dashboard/', views.dashboard),
    path('student/', views.student_management,name='student_management'),
    path('student/edit_student/<str:student_id>/', views.edit_student,name='edit_student'),
    path('student/delete_student/<str:student_id>/', views.delete_student,name='delete_student'),
    path('student/add_student/', views.add_student,name='add_student'),
    path('course/', views.course_management,name='course_management'),
    path('course/edit_course/<str:course_id>/', views.edit_course, name='edit_course'),
    path('course/delete_course/<str:course_id>/', views.delete_course, name='delete_course'),
    path('course/add_course/', views.add_course,name='add_course'),
    path('enrollment/', views.enrollment_management,name='enrollment_management'),
    path('enrollment/edit_enrollment/<str:student_id>/<str:course_id>/', views.edit_enrollment, name='edit_enrollment'),
    path('enrollment/delete_enrollment/<str:student_id>/<str:course_id>/', views.delete_enrollment, name='delete_enrollment'),
    path('enrollment/add_enrollment/', views.add_enrollment, name='add_enrollment'), #添加选课信息的url，定向到add_enrollment函数
]
```

`views.py`后端处理

```python
def add_enrollment(request):
    if request.method == 'POST': # 页面有展示有提交，当提交选课时，按照下面逻辑进行
        course_id = request.POST.get("course_id")
        student_id = request.POST.get("student_id")
        grade = request.POST.get("grade")
        if not course_id or not student_id:    # 处理前端错误
            messages.error(request, 'Course and student must be selected.')
        try:

            if Enrollments.objects.filter(student_id=student_id,course_id=course_id).exists(): # 如果已经选过这门课，不能再选
                # Display error message
                messages.error(request, "选课信息已存在！")
            else:
                # Save the student record to the database
                if not isinstance(student_id, str):
                    print("非字符串！")
                with connection.cursor() as cursor: # Django不支持复合主键，因此需要调用已经写好的存储过程  gpa计算由触发器完成
                    cursor.callproc('insert_enrollment', [student_id, course_id, grade])
                # Redirect to the student list page or any other desired page
                redirect_url = reverse('enrollment_management')  # 反解析重定向到选课管理界面
                return redirect(redirect_url)

        except Exception as e: # 错误处理
            # Display error message
            messages.error(request, "选课信息添加失败：" + str(e))
    students = Students.objects.all()# 加载页面时，把数据库中信息送入前端
    courses = Courses.objects.all()
    context = {'students':students,'courses':courses}
    return render(request,'admin_system/add_enrollment.html',context)
```

`add_enrollment.htmll`前端界面

```html
<!DOCTYPE html>
<html>
<head>
    <title>Add Enrollment</title>
    {% load static %}   <!-- 添加Django的static模板 -->
    <link rel="stylesheet" type="text/css" href="{% static 'css/edit_style.css' %}">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
</head>
<body>
    <h1>Add Enrollment</h1>

    <form method="POST" action="{% url 'add_enrollment' %}">
        {% csrf_token %}

    <label for="course_id">Course:</label>  <!-- 给出列表，只能在已有的学生和课程中选择，保证外键约束 -->
    <select name="course_id" id="course_id" required>
        <option value="">Please select a course</option>
        {% for course in courses %}
            <option value="{{ course.course_id }}">{{ course.course_id }}</option>
        {% endfor %}
    </select>

    <br>

    <label for="student_id">Student:</label>
    <select name="student_id" id="student_id" required>
        <option value="">Please select a student</option>
        {% for student in students %}
            <option value="{{ student.student_id }}">{{ student.student_id }}</option>
        {% endfor %}
    </select>

    <br>

        <label for="grade">Grade:</label>   <!-- 成绩限制 0-100 -->
        <input type="number" name="grade" id="grade" min="0" max="100" required>

        <br>

        <input type="submit" value="Add Enrollment">
    </form>
    {% if messages %}
      {% for message in messages %} <!-- 后端错误信息显示 -->
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
          {{ message }}
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      {% endfor %}
    {% endif %}
    <!-- 添加Bootstrap脚本 -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.0/dist/js/bootstrap.min.js"></script>
</body>
</html>
```

## 结果展示

**主界面**

![image-20240618152316226](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152316226.png)

**管理员操作主界面**

![image-20240618152342708](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152342708.png)

**学生管理**

![image-20240618152412722](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152412722.png)

**修改学生信息**

![image-20240618152446904](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152446904.png)

**添加学生信息，当学生ID已存在时报错**

![image-20240618152525257](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152525257.png)

**添加选课信息**

![image-20240618152610112](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152610112.png)

**学生注册和登录**

![image-20240618152715288](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152715288.png)

**学生主界面**

![image-20240618152742837](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152742837.png)

**学生选课**

![image-20240618152806421](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152806421.png)

**个人主页**

![image-20240618152840793](C:\Users\Liuz\Desktop\database\lab2\djangoProject\report.assets\image-20240618152840793.png)