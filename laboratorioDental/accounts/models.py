from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, post_delete

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('tecnico', 'Técnico'),
        ('recepcionista', 'Recepcionista'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='recepcionista')

    def __str__(self):
        return self.username

class SingletonModel(models.Model):
    """Modelo base que asegura una única instancia en la base de datos.
    Uso:
        class AppSingleton(SingletonModel):
            campo = models.CharField(...)
        instancia = AppSingleton.load()
    """

    class Meta:
        abstract = True

    # in-memory cache per subclass to return the same Python object
    _cached_instance = None
    _signals_connected = False

    def save(self, *args, **kwargs):
        # Force primary key to 1 so there's only one row.
        self.pk = 1
        super().save(*args, **kwargs)
        type(self)._cached_instance = self

    @classmethod
    def _connect_signals(cls):
        """Connect post_save/post_delete to keep the in-memory cache in sync."""
        if cls._signals_connected:
            return

        def _on_save(sender, instance, **kwargs):
            # update the cached instance to the saved object
            if isinstance(instance, cls):
                cls._cached_instance = instance

        def _on_delete(sender, instance, **kwargs):
            if isinstance(instance, cls):
                cls._cached_instance = None

        post_save.connect(_on_save, sender=cls, dispatch_uid=f"{cls.__name__}_singleton_save")
        post_delete.connect(_on_delete, sender=cls, dispatch_uid=f"{cls.__name__}_singleton_delete")
        cls._signals_connected = True

    @classmethod
    def load(cls, *, force_refresh: bool = False, check_db: bool = False):
        """Return the singleton instance.

        Parameters
        - force_refresh: if True, always re-read from the DB and update the cache.
        - check_db: if True, when a cached instance exists, compare its
          `updated` timestamp with the DB value and refresh the cache if they
          differ. This helps detect modifications made by other processes.

        Notes: caching is per-process. If the singleton is modified in another
        process, the current process will not see the change unless you
        use `force_refresh=True` or `check_db=True` to re-query the DB.
        """
        # connect signals once so cache stays consistent in this process
        cls._connect_signals()

        # Return cached unless a refresh/check is requested
        cached = getattr(cls, '_cached_instance', None)
        if cached is not None and not force_refresh and not check_db:
            return cached

        if cached is not None and check_db:
            # Compare `updated` field to detect external changes.
            try:
                db_updated = cls.objects.values_list('updated', flat=True).filter(pk=1).first()
                if db_updated is not None and db_updated == cached.updated:
                    # cache is up-to-date
                    cls._cached_instance = cached
                    return cached
            except Exception:
                # If anything goes wrong with the DB check, fall back to reload
                pass

        # Fetch/create from DB and cache it
        obj, created = cls.objects.get_or_create(pk=1)
        cls._cached_instance = obj
        return obj

    @classmethod
    def clear_cache(cls):
        """Clear the in-memory cached instance for this singleton class."""
        cls._cached_instance = None


class AppSingleton(SingletonModel):
    """Modelo singleton concreto para almacenar estado global de la app.
    Campos:
        site_name: nombre del sitio (opcional)
        login_count: cantidad de logins exitosos
        updated: última actualización
    """

    site_name = models.CharField(max_length=100, blank=True, default='LaboratorioDental')
    login_count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def increment_logins(self, by=1):
        self.login_count = (self.login_count or 0) + by
        self.save()

    def __str__(self):
        return f"AppSingleton(site_name={self.site_name} login_count={self.login_count})"
    
class Tecnico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='tecnico')
    especialidad = models.CharField(max_length=100, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario.username