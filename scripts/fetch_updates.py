import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

# ===============================
# Data ISO (ano / semana)
# ===============================
today = datetime.utcnow()
year, week, _ = today.isocalendar()

base_dir = Path("main") / str(year) / f"week_{week:02d}"
base_dir.mkdir(parents=True, exist_ok=True)

output_file = base_dir / "updates.md"

# ===============================
# Fonte IFRS
# ===============================
IFRS_URL = "https://www.ifrs.org/issued-standards/list-of-standards/"

def fetch_ifrs_updates():
    response = requests.get(IFRS_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    updates = []

    # OBS: seletor simples e conservador
    for link in soup.select("a"):
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        if "ifrs.org" not in href:
            continue

        # Heurística simples para filtrar ruído
        keywords = ["IFRS", "IAS", "Amendment", "amendment", "Standard"]
        if any(k in title for k in keywords):
            updates.append({
                "title": title,
                "url": href
            })

    # limitar para não gerar lixo
    return updates[:10]

# ===============================
# Escrita do arquivo (SOBRESCREVE)
# ===============================
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"# Atualizações Normativas – Ano {year}, Semana {week}\n\n")

    f.write("## IFRS – Issued Standards and Amendments\n\n")
    f.write(f"Fonte oficial: {IFRS_URL}\n\n")

    updates = fetch_ifrs_updates()

    if not updates:
        f.write("_Nenhuma atualização identificada automaticamente nesta semana._\n")
    else:
        for u in updates:
            f.write(f"### {u['title']}\n")
            f.write(f"- Link: {u['url']}\n\n")

    f.write("---\n")
    f.write(
        "\n➡️ **Próximo passo:** Copie os títulos ou textos relevantes acima "
        "e cole no ChatGPT usando o prompt técnico padrão para gerar o resumo contábil.\n"
    )

print(f"Arquivo sobrescrito com sucesso: {output_file}")
