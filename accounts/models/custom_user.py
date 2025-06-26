from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, nome, senha=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, senha=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nome, senha, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
    )

    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    num_celular = models.CharField(max_length=11,
                                validators=[MinLengthValidator(10, message='O número de telefone deve conter exatamente 11 dígitos.')],
                                blank=True,
                                null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    data_criacao = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome','sobrenome','tipo']

    def __str__(self):
        return f'{self.nome} ({self.tipo})'
