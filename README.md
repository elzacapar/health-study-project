## 🇬🇧 English Version

# Individual Assignment - Health Study

This repository contains the solution for the examinable submission assignment in the course Data Science/Python Programming and Statistical Data Analysis. The project involves analyzing a synthetic dataset from a health study (`health_study_dataset.csv`) and building a reusable analysis pipeline.

---

## Part 1: Basic Analysis and Statistics

* **Branch:** `del1`
* **Main File:** `del1_analysis.ipynb`
* **Content:** Descriptive statistics, simulation (disease rate), calculation of confidence intervals (Normal/Bootstrap), and hypothesis testing (Welch's t-test).

---

## Part 2: In-Depth Analysis and Pipeline

* **Branch:** `del2`
* **Main File:** `del2_pipeline.ipynb`
* **Pipeline Structure:** All logic from Part 1 and Part 2 has been moved to the **`HealthAnalyzer`** class in the module `src/health_analyzer.py`.
* **Advanced Methods:** Multiple linear regression and proportion test (extended analysis).

---

## Reproducibility and Requirements

**To run the analysis locally:**

1.  Clone the repository.
2.  Create and activate a virtual environment (`.venv`).
3.  Install dependencies from `requirements.txt`.
4.  Run `del2_pipeline.ipynb` (or `del1_analysis.ipynb`) top-to-bottom.

### Python Version
This code was based on **Python 3.11.9**.

### Dependencies
All necessary packages are listed in `requirements.txt`.


***

## 🇸🇪 Svensk Version

# Individuell Uppgift - Hälsostudie

Detta repository innehåller lösningen för den examinerande inlämningsuppgiften i kursen Data Science/Pythonprogrammering och statistisk dataanalys. Projektet går ut på att analysera ett syntetiskt dataset från en hälsostudie (`health_study_dataset.csv`) och bygga en återanvändbar analyspipeline.

---

## Del 1: Grundläggande Analys och Statistik

* **Branch:** `del1`
* **Huvudfil:** `del1_analysis.ipynb`
* **Innehåll:** Beskrivande statistik, simulering (disease rate), beräkning av konfidensintervall (Normal/Bootstrap), och hypotesprövning (Welch's t-test).

---

## Del 2: Fördjupning och Pipeline

* **Branch:** `del2`
* **Huvudfil:** `del2_pipeline.ipynb`
* **Pipeline-struktur:** All logik från Del 1 och Del 2 har flyttats till klassen `HealthAnalyzer` i modulen `src/health_analyzer.py`.
* **Avancerade Metoder:** Multipel linjär regression och proportionstest (utökad analys).

---

## Reproducerbarhet och Krav

**För att köra analysen lokalt:**

1.  Klona repositoryt.
2.  Skapa och aktivera en virtuell miljö (`.venv`).
3.  Installera beroenden från `requirements.txt`.
4.  Kör `del2_pipeline.ipynb` (eller `del1_analysis.ipynb`) top-to-bottom.

### Python-version
Denna kod baserades på **Python 3.11.9**.

### Beroenden
Alla nödvändiga paket finns listade i `requirements.txt`.