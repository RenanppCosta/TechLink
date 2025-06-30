from django.conf import settings
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from pagamentos.forms.cartao_checkout_form import CustomCheckoutForm
import json
from django.conf import settings
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from accounts.models import PerfilProfessor
from agendamentos.models import Horario

class CheckoutView(FormView):
    template_name = 'pagamentos/checkout.html'
    form_class = CustomCheckoutForm
    success_url = reverse_lazy('pagamentos:payment_success')

    def dispatch(self, request, *args, **kwargs):
        # Protege a página de ser acessada sem um agendamento iniciado
        if 'checkout_context' not in self.request.session:
            return redirect('techlink:home') # Altere para sua home
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        checkout_context = self.request.session.get('checkout_context')

        # LÊ DA SESSÃO E ENVIA PARA O TEMPLATE
        professor = get_object_or_404(PerfilProfessor, id=checkout_context['professor_id'])
        horarios = Horario.objects.filter(id__in=checkout_context['horario_ids'])
        
        context['professor'] = professor
        context['horarios_agendados'] = horarios
        context['valor_total'] = checkout_context['valor_total']
        context['valor_em_centavos'] = checkout_context['valor_em_centavos']
        context['horario_ids_json'] = json.dumps(checkout_context['horario_ids'])
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        
        return context