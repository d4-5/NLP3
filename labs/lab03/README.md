# Lab 03 — Lemma / POS

**Напрям:** B) Extraction / NER  

**Інструмент для лем/POS:** Stanza  

**Baseline:**  
- Baseline 1: регулярні вирази на оригінальному тексті (processed_v2)  
- Baseline 2: POS-патерни + леми через Stanza  

**Основні цифри (Precision):**  
- Baseline 1 (regex): 1.0  
- Baseline 2 (POS/леми): 0.8  

**Висновок:**  
Для нашого завдання витягання власних імен та організацій леми та POS не покращили точність і іноді пропускали сутності.