from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
	def __init__(self, *args, **kwargs):
		self.with_deleted = kwargs.pop('deleted', False)
		super(SoftDeleteManager, self).__init__(*args, **kwargs)

	def _base_queryset(self):
		return super().get_queryset().filter(is_deleted=False)

	def get_queryset(self):
		qs = self._base_queryset()
		if self.with_deleted:
			print('here')
			return super().get_queryset().filter(is_deleted=True)
		return qs


class SoftDeletionModel(BaseModel):
    class Meta:
        abstract = True
        
    is_deleted = models.BooleanField(null=False, default=False)
    delete_at = models.DateTimeField(null=True)

    objects = SoftDeleteManager()
    objects_with_deleted = SoftDeleteManager(deleted=True)
    objects_all = models.Manager()
    

    def delete(self):
        self.is_deleted = True
        self.delete_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()