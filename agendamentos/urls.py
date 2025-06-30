from django.urls import path
from .views import CriarAgendamentoView,AulaConcluirView,AulaCancelarView,AulaExcluirView


app_name = 'agendamentos'

urlpatterns = [
    path('agendar/<int:professor_id>/', CriarAgendamentoView.as_view(), name='criar_agendamento'),
    path('aula/<int:aula_id>/concluir/', AulaConcluirView.as_view(), name='marcar_aula_concluida'),
    path('aula/<int:aula_id>/cancelar/', AulaCancelarView.as_view(), name='cancelar_aula'),
    path('aula/<int:aula_id>/excluir/', AulaExcluirView.as_view(), name='excluir_aula'),
]
'''
urlpatterns = [
    path('agendar/<int:professor_id>/', CriarAgendamentoView.as_view(), name='criar_agendamento'),
    path('cancelar/', 'agendamentos.views.cancelar', name='cancelar'),
    path('historico/', 'agendamentos.views.historico', name='historico'),
    path('detalhes/<int:id>/', 'agendamentos.views.detalhes', name='detalhes'),
]'''