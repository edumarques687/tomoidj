from django.db import models
from django.contrib.auth.models import User


class Enhancement(models.Model):
    cost = models.CharField(max_length=30)
    effect = models.TextField()
    related_jutsu = models.ForeignKey('Jutsu', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return 'Related to: ' + self.related_jutsu.name


class Jutsu(models.Model):

    name = models.TextField()
    sorting_name = models.TextField(blank=True)
    image = models.ImageField(upload_to='jutsu/images', blank=True)

    CHACRA_CHOICES = [
        ('FO', 'Força'),
        ('DE', 'Destreza'),
        ('CO', 'Constituição'),
        ('IN', 'Inteligência'),
        ('SA', 'Sabedoria'),
        ('CA', 'Carisma'),
    ]
    chacra = models.CharField(
        max_length=2,
        choices=CHACRA_CHOICES,
        default='FO',
    )

    DESCRIPTOR_CHOICES = [
        ('AB', 'Abjuração'),
        ('AD', 'Advinhação'),
        ('EM', 'Elemental'),
        ('AC', 'Ácido'),
        ('EL', 'Eletricidade'),
        ('FO', 'Fogo'),
        ('FR', 'Frio'),
        ('VE', 'Vento'),
        ('EN', 'Encantamento'),
        ('IL', 'Ilusão'),
        ('IN', 'Invocação'),
        ('NI', 'Ninja'),
        ('LU', 'Luz'),
        ('TR', 'Transmutação'),
        ('TT', 'Trevas'),
        ('VA', 'Vácuo'),
    ]
    descriptor = models.CharField(
        max_length=2,
        choices=DESCRIPTOR_CHOICES,
        default='AB',
    )

    descriptor2 = models.CharField(
        max_length=2,
        choices=DESCRIPTOR_CHOICES,
        blank=True,
        default='',
    )
    descriptor3 = models.CharField(
        max_length=2,
        choices=DESCRIPTOR_CHOICES,
        blank=True,
        default='',
    )
    descriptor4 = models.CharField(
        max_length=2,
        choices=DESCRIPTOR_CHOICES,
        blank=True,
        default='',
    )

    GRADE_CHOICES = [
            ('BA', 'Básico'),
            ('ME', 'Mediano'),
            ('AV', 'Avançado'),
            ('SU', 'Sublime'),
            ('LE', 'Lendário'),
    ]

    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
        default='LE',
    )

    execution = models.TextField()
    range = models.TextField()
    target_area_effect = models.TextField()
    duration = models.TextField()
    resistance = models.TextField(blank=True)
    description = models.TextField(default='')
    enhancements = models.ManyToManyField(to=Enhancement, related_name='jutsu', blank=True)
    short_description = models.CharField(max_length=100, blank=True)
    book_magazine = models.CharField(max_length=100, default="Manual Básico", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="admin", null=True)

    def id(self):
        return self.id

    def __str__(self):
        return self.name


