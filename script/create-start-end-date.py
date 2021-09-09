from django.utils import timezone
from datetime import timedelta

start = timezone.now()
end = timezone.now() + timedelta(days=10)
print(start)
print(end)