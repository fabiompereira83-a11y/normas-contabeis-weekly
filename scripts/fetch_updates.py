import requests
from datetime import datetime
from pathlib import Path

OUTPUT = Path("updates_weekly.md")

sources = [
    {
        "name": "IFRS – Amendments and New Standards",
        "url": "https://www.ifrs.org/issued-standards/list-of-standards/"
    },
    {
        "name": "IFRIC – Agenda Decisions",
        "url": "https://www.ifrs.org/groups/international-financial-reporting-interpretations-committee/agenda-decisions/"
    },
    {
        "name": "CPC – Pronunciamentos",
        "url": "https://www.cpc.org.br/CPC/Pronunciamentos"
    }
]

today = datetime.utcnow().strftime("%Y-%m-%d")

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(f"# Atualizações Normativas – Semana {today}\n\n")
    f.write("Fontes monitoradas (links oficiais):\n\n")

    for s in sources:
        f.write(f"- **{s['name']}**: {s['url']}\n")

    f.write("\n---\n")
    f.write(
        "\n➡️ **Instrução:** Abra os links acima, identifique documentos novos ou revisados "
        "desde a última semana e cole o texto relevante no ChatGPT usando o prompt técnico padrão.\n"
    )

print("Arquivo updates_weekly.md gerado.")
