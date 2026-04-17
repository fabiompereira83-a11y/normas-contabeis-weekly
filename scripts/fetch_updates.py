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
# Fonte CPC (site público)
# ===============================
CPC_URL = "https://www.cpc.org.br/CPC/Documentos-Emitidos/Pronunciamentos"

def fetch_cpc_updates():
    response = requests.get(CPC_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    updates = []

    # Estrutura atual do site CPC: tabela com links
    for row in soup.select("table tr"):
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        title = cols[0].get_text(strip=True)
        link_tag = cols[0].find("a")

        if not title or not link_tag:
            continue

        link = link_tag.get("href")
        if not link.startswith("http"):
            link = f"https://www.cpc.org.br{link}"

        updates.append({
            "title": title,
            "url": link
        })


# ===============================
# Escrita do arquivo (SOBRESCREVE)
# ===============================
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"# Atualizações Normativas – Ano {year}, Semana {week}\n\n")

    f.write("## CPC – Pronunciamentos Contábeis\n\n")
    f.write(f"Fonte oficial: {CPC_URL}\n\n")

    updates = fetch_cpc_updates()

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
