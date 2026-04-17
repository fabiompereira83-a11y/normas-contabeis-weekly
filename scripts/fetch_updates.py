import requests
from datetime import datetime
from pathlib import Path

# Data atual em padrão ISO
today = datetime.utcnow()
year, week, _ = today.isocalendar()

# Estrutura de pastas: main/year/week_xx
base_dir = Path("main") / str(year) / f"week_{week:02d}"
base_dir.mkdir(parents=True, exist_ok=True)

OUTPUT = base_dir / "updates_weekly.md"

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
