from django.db import models


from base.models import SoftDeletionModel
from business.models import Business
from customer.models import Customer

class MembershipProgram(SoftDeletionModel):
    discount_percentage = models.FloatField()
    price = models.FloatField()
    description = models.CharField(max_length=200, blank=True)
    business = models.OneToOneField(Business, on_delete=models.CASCADE)
    customer = models.ManyToManyField(Customer, through='Membership')

    class Meta:
        ordering = ['id']


# when customer send a request to join the membership, set date_request
# when request is approved, set date_join and joined=True
# list membership request: 
#       MembershipProgram.objects.filter(membership__joined=False)
#       Customer.objects.filter(membership__joined=False)
# list customer have joined the membership: 
#       MembershipProgram.objects.filter(membership__joined=True)
#       Customer.objects.filter(membership__joined=True)
class Membership(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    membership = models.ForeignKey(MembershipProgram, on_delete=models.CASCADE)
    date_join = models.DateTimeField(null=True)
    date_request = models.DateTimeField(null=True)
    joined = models.BooleanField(default=False)