from django.db import models
from django.db.models.deletion import ProtectedError
from django.utils import timezone

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


class SoftDeletionModel(models.Model):
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

    # def _on_delete(self):
    #     for relation in self._meta._relation_tree:
    #         on_delete = getattr(relation.related, 'on_delete', models.DO_NOTHING)

    #         if on_delete in [None, models.DO_NOTHING]:
    #             continue

    #         snapshot_kwargs = {}

    #         if issubclass(relation.model, SoftDeletionModel):
    #             snapshot_kwargs['snapshot_id'] = self.snapshot_id

    #         filter = {relation.name: self}
    #         related_queryset = relation.model.objects.filter(**filter)

    #         if on_delete == models.CASCADE:
    #             relation.model.objects.filter(**filter).delete(**snapshot_kwargs)
    #         elif on_delete == models.PROTECT:
    #             if related_queryset.count() > 0:
    #                 raise ProtectedError()
    #         else:
    #             raise(NotImplementedError())

	
