from django import forms
from agendamentos.models import Horario
from datetime import datetime, timedelta, time

class HorarioDisponivelForm(forms.Form):
    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor')
        super().__init__(*args, **kwargs)
        hoje = datetime.today().date()
        dias = [hoje + timedelta(days=i) for i in range(7)]
        horarios = [time(h, 0) for h in range(6, 23)]
        self.dias = dias
        self.horarios = [h.strftime('%H:%M') for h in horarios]

        for dia in dias:
            for hora in horarios:
                nome = f"{dia}|{hora.strftime('%H:%M')}"
                checked = Horario.objects.filter(
                    professor=professor, data=dia, hora=hora, disponivel=True
                ).exists()
                self.fields[nome] = forms.BooleanField(
                    required=False,
                    initial=checked,
                    label='',
                    widget=forms.CheckboxInput(attrs={'class': 'inline-checkbox'})
                )