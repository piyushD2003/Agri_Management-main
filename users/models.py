from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser):
    first_name = models.CharField(
        max_length=30,
        verbose_name="First Name"
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name="Last Name"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email Address"
    )
    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Phone Number"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Is Staff"
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Is Superuser"
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="Is Admin"
    )
    is_manager = models.BooleanField(
        default=False,
        verbose_name="Is Manager"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Created"
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Date Updated"
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff or self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff or self.is_admin


class Farmer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name="farmer_profile"
        )
    farm_name = models.CharField(
        max_length=255, verbose_name="Farm Name")
    farm_location = models.CharField(max_length=255, verbose_name="Farm Location"
        )
    farm_size = models.FloatField(
        verbose_name="Farm Size (in hectares)"
        )

    def __str__(self):
        return f"Farmer: {self.user.first_name} {self.user.last_name}"
    
    city = models.CharField(
      max_length=255, verbose_name="City", null=True, blank=True
       )

    class Meta:
        db_table = "farmer"
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"


class FarmManager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, 
        related_name="farm_manager_profile"
        )
    farm_name = models.CharField(
        max_length=255,
        verbose_name="Farm Name"
        )
    farm_location = models.CharField(
        max_length=255,
        verbose_name="Farm Location"
        )
    manager_experience = models.IntegerField(
        verbose_name="Years of Experience"
        )

    def __str__(self):
        return f"Farm Manager: {self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = "farm_manager"
        verbose_name = "Farm Manager"
        verbose_name_plural = "Farm Managers"


class Farm(models.Model):
    name = models.CharField(max_length=255,
        verbose_name="Farm Name"
    )
    address = models.CharField(max_length=255,
        verbose_name="Farm Address"
    )
    location_url = models.URLField(verbose_name="Farm Location URL")
   
    farm_size = models.CharField(max_length=50, 
        verbose_name="Farm Size"
    )
    user_created = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="farms",
        verbose_name="User Created"
    )
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "farm"
        verbose_name = "Farm"
        verbose_name_plural = "Farms"