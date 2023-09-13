from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, email2, f_name, l_name, date_of_birth, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            email2=self.normalize_email(email2),
            f_name=f_name,
            l_name=l_name,
            date_of_birth=date_of_birth
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, email2, f_name, l_name, date_of_birth, password=None):
        user = self.create_user(
            email,
            email2,
            f_name=f_name,
            l_name=l_name,
            date_of_birth=date_of_birth,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    email2 = models.EmailField(
        verbose_name="secondary email address",
        max_length=255,
        blank=False
    )
    f_name = models.CharField(
        verbose_name="first name",
        max_length=255,
        blank=False
    )
    l_name = models.CharField(
        verbose_name="last name",
        max_length=255,
        blank=False
    )
    date_of_birth = models.DateField(
        verbose_name="date of birth",
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email2", "f_name", "l_name", "date_of_birth"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    