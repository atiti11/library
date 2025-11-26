# 📚 Knihovní systém v Pythonu + MySQL

Tento projekt je jednoduchý konzolový systém pro správu knihovny pomocí jazyka **Python** a databáze **MySQL**. Výsledny software (`library_solution.py`) Umožňuje:

- registraci a identifikaci členů,
- výpůjčku a vrácení knih,
- zobrazení dostupných knih a aktuálně vypůjčených knih.

> ! POZOR: při prvním spuštění databáze neobsahuje žádné uživatele ani knihy - je potřeba je doplnit ručně přes MySQL WorkBench.

## 🔧 Požadavky

- Python 3.7+
- Knihovna pro připojení k mysql serveru (jedna z násleudjících):
  - [`mysql-connector-python`](https://pypi.org/project/mysql-connector-python/)
- MySQL server (např. MariaDB nebo MySQL Community Server)

Nainstaluj potřebné balíčky:

```bash
pip install mysql-connector-python
```

## Úkoly v kódu

Soubor `library.py` obsahuje několik komentářů označený jako "TODO". Tyto komentáře pospiují, co je potřeba v projektu doplnit, aby fungoval (jedná se o věci spojené s databází). Soubor `library_solution.py` obsahuje, jak by měl vypadat výsledek. Složka `/mysql_examples/` obsahuje příklady použití knihovny mysql.
