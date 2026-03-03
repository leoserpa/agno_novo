"""Personal Tech Advocate — Agente de IA com Agno + Gemini.

Este agente analisa os repositórios públicos de um usuário do GitHub
e gera um relatório profissional sobre as competências técnicas do
desenvolvedor, focado em vagas de Análise e Ciência de Dados.
"""

# ============================================================
# PASSO 1 — Importação de bibliotecas
# ============================================================
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.github import GithubTools
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (ex: GOOGLE_API_KEY e GITHUB_ACCESS_TOKEN)
load_dotenv()


# ============================================================
# PASSO 2 — Configuração da Ferramenta Nativa (GithubTools)
# ============================================================
# O Agno já fornece uma tool pronta que faz dezenas de operações no GitHub.
ferramenta_github = GithubTools(
    # Quais poderes daremos ao agente?
    search_repositories=True, # 🔍 Permite ao agente buscar repositórios
    get_repository=True, # 📦 Permite acessar os detalhes de um repo específico
    read_repository_file=True, # 🔥 O agente poderá LER seus arquivos (ex: README)
    list_pull_requests=False, # ❌ Desativado (não analisaremos Pull Requests)
    list_issues=False, # ❌ Desativado (não analisaremos Issues no repositório)
    list_user_repositories=True, # 👤 Permite listar TODOS os seus repositórios
)


# ============================================================
# PASSO 3 — Configuração do Agente Agno
# ============================================================
agente = Agent(
    # --- Modelo de IA ---
    model=Gemini(id="gemini-2.5-flash"),

    # --- Ferramentas disponíveis para o agente ---
    tools=[ferramenta_github],

    # --- Instruções de comportamento do agente ---
    instructions=[
        "Você é o 'Personal Tech Advocate', um especialista em apresentar "
        "desenvolvedores para recrutadores de tecnologia.",
        "Seu fluxo de trabalho DEVE ser:",
        "  1. Buscar a lista de repositórios do usuário solicitado.",
        "  2. Escolher os 3 repositórios mais focados em Dados/Python/SQL.",
        "  3. Ler o conteúdo do arquivo 'README.md' desses 3 repositórios "
        "     para entender profundamente a qualidade do código e da documentação.",
        "Com base em toda essa investigação, gere um relatório profissional "
        "e persuasivo 'vendendo' o perfil candidato para uma vaga de Dados.",
        "Organize o relatório com seções claras: Resumo do Perfil, "
        "Competências Técnicas, Análise da Documentação (baseada nos READMEs que você leu) "
        "e Projetos de Destaque.",
        "Use um tom confiante e positivo.",
    ],

    # --- Configurações de exibição ---
    markdown=True,
    debug_mode=True, # Deixa isso True para você ver ele lendo os arquivos!
)


# ============================================================
# PASSO 4 — Execução do agente
# ============================================================
if __name__ == "__main__":
    usuario = "leoserpa"

    agente.print_response(
        f"Analise o perfil do GitHub do usuário '{usuario}' e gere o relatório."
    )
