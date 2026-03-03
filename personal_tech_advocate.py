"""Personal Tech Advocate — Agente de IA com Agno + Gemini.

Este agente analisa os repositórios públicos de um usuário do GitHub
e gera um relatório profissional sobre as competências técnicas do
desenvolvedor, focado em vagas de Análise e Ciência de Dados.
"""

# ============================================================
# PASSO 1 — Importação de bibliotecas
# ============================================================
import json

import requests
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (ex: GOOGLE_API_KEY)
load_dotenv()


# ============================================================
# PASSO 2 — Ferramenta (Tool) de busca no GitHub
# ============================================================
def buscar_repositorios_github(username: str) -> str:
    """Busca os repositórios públicos de um usuário no GitHub.

    Essa função acessa a API pública do GitHub, coleta informações
    relevantes de cada repositório e retorna um resumo em formato JSON.

    Args:
        username: Nome de usuário do GitHub (ex: "torvalds").

    Returns:
        String JSON contendo a lista de repositórios com nome,
        descrição, linguagem principal, tópicos, estrelas e URL.
    """
    url = f"https://api.github.com/users/{username}/repos"

    resposta = requests.get(url, timeout=10)

    if resposta.status_code != 200:
        return json.dumps({
            "erro": f"Não foi possível acessar o perfil '{username}'. "
                    f"Status HTTP: {resposta.status_code}"
        })

    repositorios_raw = resposta.json()

    repositorios = []
    for repo in repositorios_raw:
        repositorios.append({
            "nome": repo.get("name", ""),
            "descricao": repo.get("description", "Sem descrição"),
            "linguagem": repo.get("language", "Não identificada"),
            "topicos": repo.get("topics", []),
            "estrelas": repo.get("stargazers_count", 0),
            "url": repo.get("html_url", ""),
        })

    return json.dumps(repositorios, ensure_ascii=False, indent=2)


# ============================================================
# PASSO 3 — Configuração do Agente Agno
# ============================================================
agente = Agent(
    # --- Modelo de IA ---
    model=Gemini(id="gemini-2.5-flash"),

    # --- Ferramentas disponíveis para o agente ---
    tools=[buscar_repositorios_github],

    # --- Instruções de comportamento do agente ---
    instructions=[
        "Você é o 'Personal Tech Advocate', um especialista em apresentar "
        "desenvolvedores para recrutadores de tecnologia.",
        "Seu foco é em habilidades de Análise e Ciência de Dados.",
        "Ao analisar os repositórios, procure ATIVAMENTE por:",
        "  - Bibliotecas: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn",
        "  - Linguagens: Python, SQL, R",
        "  - Tipos de arquivo: Jupyter Notebooks (.ipynb), scripts .py",
        "  - Projetos de BI: arquivos Power BI (.pbix), dashboards",
        "  - Qualidade da documentação nos READMEs",
        "Gere um relatório profissional e persuasivo 'vendendo' o perfil "
        "do candidato para uma vaga na área de Dados.",
        "Organize o relatório com seções claras: Resumo do Perfil, "
        "Competências Técnicas, Projetos de Destaque e Recomendação Final.",
        "Use um tom confiante e positivo, como um headhunter que acredita "
        "no potencial do candidato.",
    ],

    # --- Configurações de exibição ---
    markdown=True,
    debug_mode=True,
)


# ============================================================
# PASSO 4 — Execução do agente
# ============================================================
if __name__ == "__main__":
    usuario = input("🔎 Digite o username do GitHub que deseja analisar: ").strip()

    agente.print_response(
        f"Analise o perfil do GitHub do usuário '{usuario}' e gere um "
        "relatório completo das competências técnicas para recrutadores "
        "da área de Dados."
    )
