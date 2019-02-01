Introduction


-------Developers Note--------
1) Server
    1.1 To Start Server, run command:
        - python manage.py runserver ip-address-to-run:port

2) Database:
    2.1 To create/update table, edit models.py
        - Class = Table in database
        - Class attributes = attributes in database
        - FieldType and Field option can be found on https://docs.djangoproject.com/en/2.1/ref/models/fields/
    
    2.2 To update changes on sqlite3, run commands:
        - python manage.py makemigrations
        - python manage.py migrate

    2.3 To see migration in terms of SQL queries, run command:
        - python manage.py sqlmigrate [application_name] [migration_number]
        - E.g My application = main, migration number = 0002,
            -> python manage.py sqlmigrate main 0001

3) Admin
    3.1 To create super use, run command:
        - python manage.py createsuperuser

    3.2 To See the tables in Admin Panel
        - Update admin.py
            -> Register the model (Class)
            -> E.g admin.site.register(Test_Class)

    3.3 To beautify Admin panel
        - create a Class Model with admin.ModelAdmin in admin.py
        - ref to https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#modeladmin-objects
        - register the model either using @admin.register(Class) wrapper or admin.site.register(Class, ClassModel)
            - E.g admin.site.register(Test, TestModel)