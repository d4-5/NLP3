import stanza


def build_pipeline():
    return stanza.Pipeline("uk", processors="tokenize,pos,lemma", use_gpu=False)


def extract_ling_features(text, nlp):
    doc = nlp(text)

    lemmas = []
    upos_tags = []

    for sent in doc.sentences:
        for word in sent.words:
            lemmas.append(word.lemma)
            upos_tags.append(word.upos)

    return {"lemma_text": " ".join(lemmas), "pos_text": " ".join(upos_tags)}
