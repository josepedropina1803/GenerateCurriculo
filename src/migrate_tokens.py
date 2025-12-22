"""
Script de migração para adicionar tokens de acesso aos currículos antigos
"""
import os
import json
import secrets

DATA_FOLDER = 'data'
METADATA_FILE = os.path.join(DATA_FOLDER, 'curriculos.json')


def generate_access_token():
    """Gera um token de acesso único e seguro"""
    return secrets.token_urlsafe(32)


def migrate_curriculos():
    """Adiciona tokens aos currículos que não têm"""
    if not os.path.exists(METADATA_FILE):
        print("Nenhum ficheiro de metadados encontrado.")
        return

    # Carrega metadados
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    updated_count = 0

    # Adiciona tokens aos currículos sem tokens
    for curriculo in metadata:
        if 'access_token' not in curriculo or not curriculo['access_token']:
            curriculo['access_token'] = generate_access_token()
            updated_count += 1
            print(f"✓ Token adicionado ao currículo de {curriculo['username']} (ID: {curriculo['id']})")

    # Guarda metadados atualizados
    if updated_count > 0:
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Migração completa! {updated_count} currículo(s) atualizado(s).")
    else:
        print("✅ Todos os currículos já têm tokens de acesso.")


if __name__ == '__main__':
    print("🔄 Iniciando migração de currículos...\n")
    migrate_curriculos()