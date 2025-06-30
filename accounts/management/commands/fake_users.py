import os
import random
from datetime import datetime, timedelta, time
from faker import Faker
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from accounts.models import CustomUser, PerfilAluno, PerfilProfessor, Tema
from agendamentos.models import Horario

fake = Faker()

def gerar_imagem_fake():
    from PIL import Image
    from io import BytesIO

    image = Image.new('RGB', (100, 100), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue(), name=f"{fake.uuid4()}.jpg")

class Command(BaseCommand):
    help = 'Cria usuários falsos do tipo aluno e professor com perfis, fotos, temas e horários'

    def handle(self, *args, **kwargs):
        # Lista fixa de temas
        temas_nomes = [
            "Matemática", "Física", "Química", "Biologia", "História",
            "Geografia", "Português", "Inglês", "Programação", "Filosofia",
            "Python","CSS","HTML","Django"
        ]

        # Criar temas se ainda não existirem
        temas = []
        for nome in temas_nomes:
            tema, _ = Tema.objects.get_or_create(nome=nome)
            temas.append(tema)

        # Criar 10 alunos
        for i in range(10):
            nome = fake.first_name()
            sobrenome = fake.last_name()
            email = nome + sobrenome + str(i) + '@email.com'
            senha = 'senha123'
            user = CustomUser.objects.create_user(
                email=email,
                nome=nome,
                sobrenome=sobrenome,
                tipo='aluno',
                senha=senha,
                num_celular=fake.msisdn()[:11],
            )
            user.foto_perfil.save(*gerar_imagem_fake().name.split('/'), content=gerar_imagem_fake())
            PerfilAluno.objects.create(usuario=user)

        # Criar 30 professores
        for i in range(30):
            nome = fake.first_name()
            sobrenome = fake.last_name()
            email = nome + sobrenome + str(i) + '@email.com'
            senha = 'senha123'
            user = CustomUser.objects.create_user(
                email=email,
                nome=nome,
                sobrenome=sobrenome,
                tipo='professor',
                senha=senha,
                num_celular=fake.msisdn()[:11],
            )
            user.foto_perfil.save(*gerar_imagem_fake().name.split('/'), content=gerar_imagem_fake())
            perfil = PerfilProfessor.objects.create(
                usuario=user,
                apresentacao=fake.paragraph(),
                valor_hora=round(random.uniform(50, 200), 2)
            )
            perfil.temas.set(random.sample(temas, k=random.randint(1, len(temas))))

            # Criar horários disponíveis para os próximos 7 dias entre 6h e 21h

            for dia in range(7):
                data = datetime.now().date() + timedelta(days=dia)
                horarios_disponiveis = random.sample(range(6, 22), k=random.randint(2, 6))# entre 2 e 6 horários por dia
                for hora_int in horarios_disponiveis:
                    hora = time(hour=hora_int)
                    Horario.objects.create(
                        professor=perfil,
                        data=data,
                        hora=hora,
                        disponivel=True
                    )


        self.stdout.write(self.style.SUCCESS('Usuários, perfis, temas e horários criados com sucesso.'))
