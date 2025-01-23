from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that includes common fields for soft deletion and timestamps.

    Attributes:
        created_at (DateTimeField): The date and time when the object was created. Automatically set on creation.
        updated_at (DateTimeField): The date and time when the object was last updated. Automatically updated on save.
        is_deleted (BooleanField): Indicates whether the object is soft-deleted. Defaults to False.
        deleted_at (DateTimeField): The date and time when the object was soft-deleted. Can be null or blank.

    Meta:
        abstract (bool): Specifies that this model is an abstract base class.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class BaseModelWithoutDelete(models.Model):
    """
    Abstract base model that includes common timestamp fields for creation and updates.

    Attributes:
        created_at (DateTimeField): The date and time when the object was created. Automatically set on creation.
        updated_at (DateTimeField): The date and time when the object was last updated. Automatically updated on save.

    Meta:
        abstract (bool): Specifies that this model is an abstract base class.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True