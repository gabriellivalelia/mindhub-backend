# Script para traduzir todas as mensagens de erro do backend
# Execute com: python traduzir_mensagens.py

TRANSLATIONS = {
    # Use Cases - Psychologist
    "Psychologist not found.": "Psicólogo não encontrado.",
    "Duplicated e-mail, cpf or crp.": "E-mail, CPF ou CRP duplicado.",
    "One or more specialties were not found.": "Uma ou mais especialidades não foram encontradas.",
    "One or more approaches were not found.": "Uma ou mais abordagens não foram encontradas.",
    "Cannot add an availability on a past date.": "Não é possível adicionar disponibilidade em uma data passada.",
    # Use Cases - Specialty e Approach
    "Specialty not found.": "Especialidade não encontrada.",
    "Approach not found.": "Abordagem não encontrada.",
    # Use Cases - Content
    "Content not found": "Conteúdo não encontrado",
    "Only psychologists can create content": "Apenas psicólogos podem criar conteúdo",
    "Only the author can delete this content": "Apenas o autor pode deletar este conteúdo",
    "Only the author can update this content": "Apenas o autor pode atualizar este conteúdo",
    # Use Cases - Appointment
    "Appointment not found": "Consulta não encontrada",
    "Appointment not found.": "Consulta não encontrada.",
    "Not authorized to cancel this appointment.": "Não autorizado a cancelar esta consulta.",
    "Not authorized to reschedule this appointment.": "Não autorizado a reagendar esta consulta.",
    "Cannot reschedule to a past date.": "Não é possível reagendar para uma data passada.",
    # Use Cases - User
    "User not found.": "Usuário não encontrado.",
    "Failed to delete user.": "Falha ao deletar usuário.",
    # Use Cases - Session/Login
    "Wrong e-mail or password": "E-mail ou senha incorretos",
    # Infra - Local File Service
    "File with key": "Arquivo com chave",
    "does not exist.": "não existe.",
    "Failed to delete file": "Falha ao deletar arquivo",
    # Infra - Session Provider
    "Missing Authorization header": "Cabeçalho de Autorização ausente",
    "Invalid Authorization header format": "Formato do cabeçalho de Autorização inválido",
    "Invalid or expired token": "Token inválido ou expirado",
    "User not found": "Usuário não encontrado",
    # Infra - Mappers
    "Invalid model type": "Tipo de modelo inválido",
    "Invalid entity type": "Tipo de entidade inválida",
}

import os


def translate_file(filepath):
    """Traduz as mensagens em um arquivo Python"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        for english, portuguese in TRANSLATIONS.items():
            # Busca por padrões: raise Exception("mensagem") ou "mensagem"
            content = content.replace(f'"{english}"', f'"{portuguese}"')
            content = content.replace(f"'{english}'", f"'{portuguese}'")

        # Só escreve se houve mudanças
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Erro ao processar {filepath}: {e}")
        return False


def main():
    base_path = "/home/gabrielli-valelia/UFMG/2025.2/Análise, projeto e programação orientados a objetos/MindHub/mindhub-backend/src"

    # Diretórios para traduzir
    directories = [
        "application/use_cases",
        "infra/services",
        "infra/providers",
        "infra/mappers",
    ]

    total_files = 0
    translated_files = 0

    for directory in directories:
        full_path = os.path.join(base_path, directory)
        for root, dirs, files in os.walk(full_path):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    total_files += 1
                    if translate_file(filepath):
                        translated_files += 1
                        print(f"✓ Traduzido: {filepath}")

    print(f"\n{'=' * 60}")
    print(f"Total de arquivos processados: {total_files}")
    print(f"Arquivos traduzidos: {translated_files}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
