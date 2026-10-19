from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Medicao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="medicoes"
    )
    sistolica = models.PositiveIntegerField(
        "Sistólica (máx.)", validators=[MinValueValidator(50), MaxValueValidator(300)]
    )
    diastolica = models.PositiveIntegerField(
        "Diastólica (mín.)", validators=[MinValueValidator(30), MaxValueValidator(200)]
    )
    pulso = models.PositiveIntegerField(
        "Pulso (bpm)",
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(250)],
    )
    data_hora = models.DateTimeField("Data e hora", default=timezone.now)
    observacao = models.CharField("Observação", max_length=200, blank=True)

    class Meta:
        ordering = ["-data_hora"]
        verbose_name = "medição"
        verbose_name_plural = "medições"

    def __str__(self):
        return f"{self.sistolica}/{self.diastolica} mmHg ({self.data_hora:%d/%m/%Y %H:%M})"

    @property
    def classificacao(self):
        """Classificação simplificada (referência: diretrizes brasileiras)."""
        s, d = self.sistolica, self.diastolica
        if s >= 180 or d >= 110:
            return ("Hipertensão grau 3", "perigo")
        if s >= 160 or d >= 100:
            return ("Hipertensão grau 2", "alto")
        if s >= 140 or d >= 90:
            return ("Hipertensão grau 1", "alerta")
        if s >= 130 or d >= 85:
            return ("Pré-hipertensão", "atencao")
        if s < 90 or d < 60:
            return ("Pressão baixa", "baixa")
        return ("Normal", "normal")

    @property
    def classe_nome(self):
        return self.classificacao[0]

    @property
    def classe_css(self):
        return self.classificacao[1]
