from user.models import User
from employee.models import Employee

user = User.objects.create(
    first_name='jean',
    last_name='lannes',
    is_staff=True,
    is_superuser=True,
    email='admin@gmail.com',
    username='jeanlannes'
)

user.set_password('admin')
user.save()

em = Employee.objects.create(
    role='admin',
    salary=999,
    user=user
)

em.save()