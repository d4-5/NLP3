import re

UA_ABBR = [
    "вул.",
    "м.",
    "р.",
    "ч.",
    "ст.",
    "кв.",
    "с.",
    "п.",
    "див.",
    "ім.",
    "т.д.",
    "т.і.",
    "млн.",
    "млрд.",
    "грн.",
]

ABBR_PATTERN = (
    r"(?<!\w)(?:"
    + "|".join(re.escape(x) for x in sorted(UA_ABBR, key=len, reverse=True))
    + r")"
)
DECIMAL_PATTERN = r"\d+\.\d+"
VERSION_PATTERN = r"(?:\d+\.){2,}\d+"
EMAIL_PATTERN = r"\b[a-zA-Z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
URL_PATTERN = r"\b(?:https?://|www\.)[^\s<>()]+"
PHONE_GENERIC_PATTERN = r"(?<!\w)\+?\d[\d\s()\-]{8,}\d(?!\w)"
PHONE_UA_PATTERN = r"\b0\d{9}\b"


def sentence_split(text: str):
    protected_tokens = {}
    counter = 0

    def protect(match):
        nonlocal counter
        key = f"__PROTECT_{counter}__"
        protected_tokens[key] = match.group(0)
        counter += 1
        return key

    text = re.sub(ABBR_PATTERN, protect, text)
    text = re.sub(VERSION_PATTERN, protect, text)
    text = re.sub(DECIMAL_PATTERN, protect, text)

    split_token = "__SENT_SPLIT__"
    text = re.sub(r'([.!?]["\')\]]+)\s+', r"\1" + split_token, text)
    text = re.sub(r"([.!?])\s+", r"\1" + split_token, text)
    sentences = text.split(split_token)

    restored_sentences = []
    for sent in sentences:
        for key, val in protected_tokens.items():
            sent = sent.replace(key, val)
        sent = sent.strip()
        if sent:
            restored_sentences.append(sent)

    return restored_sentences


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\t", " ")

    text = re.sub(
        r'(?:(?<=^)|(?<=[\s(\[{—–-]))(["«“»”])\s+(?=[A-Za-zА-Яа-яІіЇїЄєҐґ\'"])',
        r"\1",
        text,
    )
    text = re.sub(r'(\S)\s+(["«“»”])(?=[\s.,!?;:)\]}-]|$)', r"\1\2", text)

    text = re.sub(r"\s+([.,!?;:)\]»”])", r"\1", text)
    text = re.sub(r"([\(\[«“])\s+", r"\1", text)

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_text(text: str) -> str:
    replacements = {
        "–": "-",
        "—": "-",
        "«": '"',
        "»": '"',
        "“": '"',
        "”": '"',
        "’": "'",
        "‘": "'",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def mask_pii(text: str) -> str:
    def mask_url_keep_trailing_punct(match: re.Match) -> str:
        url = match.group(0)
        trailing = ""
        while url and url[-1] in ".,!?;:)":
            trailing = url[-1] + trailing
            url = url[:-1]
        return "<URL>" + trailing

    text = re.sub(URL_PATTERN, mask_url_keep_trailing_punct, text)
    text = re.sub(EMAIL_PATTERN, "<EMAIL>", text)
    text = re.sub(PHONE_UA_PATTERN, "<PHONE>", text)

    def mask_phone_if_valid(match: re.Match) -> str:
        phone = match.group(0)
        digits_only = re.sub(r"\D", "", phone)
        if 10 <= len(digits_only) <= 15:
            return "<PHONE>"
        return phone

    text = re.sub(PHONE_GENERIC_PATTERN, mask_phone_if_valid, text)
    return text


def preprocess(text: str) -> dict:
    text = normalize_text(text)
    text = clean_text(text)
    text = mask_pii(text)
    sentences = sentence_split(text)

    return {"clean": text, "sentences": sentences}
