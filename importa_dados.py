import os
import sys
import csv
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.culturas.models import Cultura
from apps.solos.models import Solo

def importar_solos(csv_file='solo.csv'):
    """Importa dados de solos a partir de um arquivo CSV"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            solos_criados = 0
            
            for row in reader:
                solo, created = Solo.objects.get_or_create(
                    nome=row['nome'],
                    defaults={
                        'descricao': row['descricao'],
                        'capacidade_campo': float(row['capacidade_campo']),
                        'ponto_murcha': float(row['ponto_murcha']),
                        'densidade': float(row['densidade']),
                        'condutividade_hidraulica': float(row['condutividade_hidraulica'])
                    }
                )
                
                if created:
                    solos_criados += 1
                    print(f"Solo criado: {solo.nome}")
                else:
                    print(f"Solo já existe: {solo.nome}")
            
            print(f"\nTotal de solos criados: {solos_criados}")
            
    except FileNotFoundError:
        print(f"Arquivo {csv_file} não encontrado!")
    except Exception as e:
        print(f"Erro ao importar solos: {e}")

def importar_culturas(csv_file='cultura.csv'):
    """Importa dados de culturas a partir de um arquivo CSV"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            culturas_criadas = 0
            
            for row in reader:
                cultura, created = Cultura.objects.get_or_create(
                    nome=row['nome'],
                    defaults={
                        'kc_inicial': float(row['kc_inicial']),
                        'kc_medio': float(row['kc_medio']),
                        'kc_final': float(row['kc_final']),
                        'z_min': float(row['z_min']),
                        'z_max': float(row['z_max']),
                        'p': float(row['p'])
                    }
                )
                
                if created:
                    culturas_criadas += 1
                    print(f"Cultura criada: {cultura.nome}")
                else:
                    print(f"Cultura já existe: {cultura.nome}")
            
            print(f"\nTotal de culturas criadas: {culturas_criadas}")
            
    except FileNotFoundError:
        print(f"Arquivo {csv_file} não encontrado!")
    except Exception as e:
        print(f"Erro ao importar culturas: {e}")

def limpar_dados():
    """Limpa todos os dados existentes (opcional)"""
    confirmacao = input("Deseja limpar todos os dados existentes? (s/n): ")
    if confirmacao.lower() == 's':
        Solo.objects.all().delete()
        Cultura.objects.all().delete()
        print("Dados limpos!")
    else:
        print("Operação cancelada.")

def menu_principal():
    """Menu interativo para importação de dados"""
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE IMPORTACAO DE DADOS")
        print("="*50)
        print("1. Importar Solos")
        print("2. Importar Culturas")
        print("3. Importar Tudo")
        print("4. Limpar Dados (CUIDADO!)")
        print("5. Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            arquivo = input("Nome do arquivo CSV (enter para solo.csv): ") or 'solo.csv'
            importar_solos(arquivo)
        elif opcao == '2':
            arquivo = input("Nome do arquivo CSV (enter para cultura.csv): ") or 'cultura.csv'
            importar_culturas(arquivo)
        elif opcao == '3':
            importar_solos()
            importar_culturas()
        elif opcao == '4':
            limpar_dados()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == '__main__':
    # Executar diretamente ou via menu
    if len(sys.argv) > 1:
        # Modo direto: python import_data.py solo.csv cultura.csv
        for arg in sys.argv[1:]:
            if 'solo' in arg.lower():
                importar_solos(arg)
            elif 'cultura' in arg.lower():
                importar_culturas(arg)
    else:
        # Modo interativo
        menu_principal()