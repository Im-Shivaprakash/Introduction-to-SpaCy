import spacy
nlp = spacy.load("en_core_web_sm")
nlp


#Doc Object
introduction_doc = nlp("This tutorial is about Natural Language Processing in spaCy.")
type(introduction_doc)
[token.text for token in introduction_doc]


#Reading from a text file
import pathlib
file_name = "introduction.txt"
introduction_doc = nlp(pathlib.Path(file_name).read_text(encoding="utf-8"))
print ([token.text for token in introduction_doc])


#Sentence Detection
about_text = ("Gus Proto is a Python developer currently working for a London-based Fintech company. He is interested in learning Natural Language Processing." )
about_doc = nlp(about_text)
sentences = list(about_doc.sents)
len(sentences)

for sentence in sentences:
    print(f"{sentence[:5]}...")


#Custom Function for space detection
ellipsis_text = ("Gus, can you, ... never mind, I forgot what I was saying. So, do you think we should ...")
from spacy.language import Language

@Language.component("set_custom_boundaries")
def set_custom_boundaries(doc):
    for token in doc[:-1]:
        if token.text == "...":
            doc[token.i + 1].is_sent_start = True
    return doc

custom_nlp = spacy.load("en_core_web_sm")
custom_nlp.add_pipe("set_custom_boundaries", before="parser")
custom_ellipsis_doc = custom_nlp(ellipsis_text)
custom_ellipsis_sentences = list(custom_ellipsis_doc.sents)
for sentence in custom_ellipsis_sentences:
    print(sentence)


#Tokenization & its attributes
about_text = ("Gus Proto is a Python developer currently working for a London-based Fintech company. He is interested in learning Natural Language Processing." )
about_doc = nlp(about_text)

for token in about_doc:
    print(token, token.idx)


print(
    f"{'Text with Whitespace':22}"
    f"{'Is Alphanum?':15}"
    f"{'Is Punctuation?':18}"
    f"{'Is Stop Word?'}"
)

for token in about_doc:
    print(
        f"{str(token.text_with_ws):22}"  #token with white space
        f"{str(token.is_alpha):15}"  #token with capital letter
        f"{str(token.is_punct):18}"  #is the token a punctutation?
        f"{str(token.is_stop)}"  #is the token a stop word?
    )

custom_about_text = (
    "Gus Proto is a Python developer currently"
    " working for a London@based London-based Fintech"
    " company. He is interested in learning"
    " Natural Language Processing."
)

print([token.text for token in nlp(custom_about_text)[8:15]])

from spacy.tokenizer import Tokenizer
custom_nlp = spacy.load("en_core_web_sm")
prefix_re = spacy.util.compile_prefix_regex(custom_nlp.Defaults.prefixes)
suffix_re = spacy.util.compile_suffix_regex(custom_nlp.Defaults.suffixes)
custom_infixes = [r"@"]
infix_re = spacy.util.compile_infix_regex(
    list(custom_nlp.Defaults.infixes) + custom_infixes
)
custom_nlp.tokenizer = Tokenizer(
    nlp.vocab,
    prefix_search=prefix_re.search,
    suffix_search=suffix_re.search,
    infix_finditer=infix_re.finditer,
    token_match=None,
)
custom_tokenizer_about_doc = custom_nlp(custom_about_text)
print([token.text for token in custom_tokenizer_about_doc[8:15]])


#Stop-words
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
len(spacy_stopwords)

for stop_word in list(spacy_stopwords)[:10]:
    print(stop_word)

custom_about_text = (
    "Gus Proto is a Python developer currently"
    " working for a London@based London-based Fintech"
    " company. He is interested in learning"
    " Natural Language Processing."
)
about_doc = nlp(custom_about_text)
for token in about_doc:
    if not token.is_stop:
        print(token)


#Lemmatization
conference_help_text = (
    "Gus is helping organize a developer"
    " conference on Applications of Natural Language"
    " Processing. He keeps organizing local Python meetups"
    " and several internal talks at his workplace."
)
conference_help_doc = nlp(conference_help_text)
for token in conference_help_doc:
    if str(token) != str(token.lemma_):
        print(f"{str(token):>20} : {str(token.lemma_)}")


#Word Frequency
from collections import Counter
complete_text = (
    "Gus Proto is a Python developer currently"
    " working for a London-based Fintech company. He is"
    " interested in learning Natural Language Processing."
    " There is a developer conference happening on 21 July"
    ' 2019 in London. It is titled "Applications of Natural'
    ' Language Processing". There is a helpline number'
    " available at +44-1234567891. Gus is helping organize it."
    " He keeps organizing local Python meetups and several"
    " internal talks at his workplace. Gus is also presenting"
    ' a talk. The talk will introduce the reader about "Use'
    ' cases of Natural Language Processing in Fintech".'
    " Apart from his work, he is very passionate about music."
    " Gus is learning to play the Piano. He has enrolled"
    " himself in the weekend batch of Great Piano Academy."
    " Great Piano Academy is situated in Mayfair or the City"
    " of London and has world-class piano instructors."
)

complete_doc = nlp(complete_text)
words = [
    token.text
    for token in complete_doc
    if not token.is_stop and not token.is_punct
]
word_freq = Counter(words)
common_words = word_freq.most_common(5)
print(common_words)


#Parts Of Speech Tagging
for token in about_doc:
    print(
        f"""
        TOKEN: {str(token)}
        =====
        TAG: {str(token.tag_):10} POS: {token.pos_}
        EXPLANATION: {spacy.explain(token.tag_)}"""
    )

nouns = []
adjectives = []
for token in about_doc:
    if token.pos_ == "ADJ":
        adjectives.append(token)

    elif token.pos_ == "NOUN":
        nouns.append(token)

print(f"{nouns = }")

print(f"{adjectives = }")


#Visualization
from spacy import displacy
about_interest_text = (
    "He is interested in learning Natural Language Processing."
)
about_interest_doc = nlp(about_interest_text)
displacy.serve(about_interest_doc, style="dep")


#Preprocessing
complete_text = (
    "Gus Proto is a Python developer currently"
    " working for a London-based Fintech company. He is"
    " interested in learning Natural Language Processing."
    " There is a developer conference happening on 21 July"
    ' 2019 in London. It is titled "Applications of Natural'
    ' Language Processing". There is a helpline number'
    " available at +44-1234567891. Gus is helping organize it."
    " He keeps organizing local Python meetups and several"
    " internal talks at his workplace. Gus is also presenting"
    ' a talk. The talk will introduce the reader about "Use'
    ' cases of Natural Language Processing in Fintech".'
    " Apart from his work, he is very passionate about music."
    " Gus is learning to play the Piano. He has enrolled"
    " himself in the weekend batch of Great Piano Academy."
    " Great Piano Academy is situated in Mayfair or the City"
    " of London and has world-class piano instructors."
)

complete_doc = nlp(complete_text)
def is_token_allowed(token):
    return bool(
        token
        and str(token).strip()
        and not token.is_stop
        and not token.is_punct
    )


def preprocess_token(token):
    return token.lemma_.strip().lower()


complete_filtered_tokens = [
    preprocess_token(token)
    for token in complete_doc
    if is_token_allowed(token)
]

print(complete_filtered_tokens)

#Rule Based matching
from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab)

about_text = ("Gus Proto is a Python developer currently working for a London-based Fintech company. He is interested in learning Natural Language Processing." )
about_doc = nlp(about_text)

def extract_full_name(nlp_doc):
    pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    matcher.add("FULL_NAME", patterns=[pattern])
    matches = matcher(nlp_doc)
    for _, start, end in matches:
        span = nlp_doc[start:end]
        return span.text
    
print(extract_full_name(about_doc))

#Dependency Parsing Using spaCy
piano_text = "Gus is learning piano"
piano_doc = nlp(piano_text)
for token in piano_doc:
    print(
        f"""
TOKEN: {token.text}
=====
{token.tag_ = }
{token.head.text = }
{token.dep_ = }"""
    )

displacy.serve(piano_doc, style="dep")

#Tree and Subtree Navigation
one_line_about_text = (
    "Gus Proto is a Python developer"
    " currently working for a London-based Fintech company"
)
one_line_about_doc = nlp(one_line_about_text)

print([token.text for token in one_line_about_doc[5].children])

print(one_line_about_doc[5].nbor(-1))

print(one_line_about_doc[5].nbor())

print([token.text for token in one_line_about_doc[5].lefts])

print([token.text for token in one_line_about_doc[5].rights])

print(list(one_line_about_doc[5].subtree))

#Shallow Parsing
#  1. Noun Phrase Detection:

import spacy
nlp = spacy.load("en_core_web_sm")
conference_text = ("There is a developer conference happening on 21 July 2019 in London.")
conference_doc = nlp(conference_text)
for chunk in conference_doc.noun_chunks:
    print(chunk)

#  2. Verb Phrase Detection:

import textacy
about_talk_text = (
    "In this talk, the speaker will introduce the audience to the use"
    " cases of Natural Language Processing in Fintech, making use of"
    " interesting examples along the way."
)
patterns = [{"POS": "AUX"}, {"POS": "VERB"}]
about_talk_doc = textacy.make_spacy_doc(about_talk_text, lang="en_core_web_sm")
verb_phrases = textacy.extract.token_matches(about_talk_doc, patterns=patterns)

for chunk in verb_phrases:
    print(chunk.text)

for chunk in about_talk_doc.noun_chunks:
    print(chunk)


#Named Entity Recognition
piano_class_text = (
    "Great Piano Academy is situated"
    " in Mayfair or the City of London and has"
    " world-class piano instructors."
)
piano_class_doc = nlp(piano_class_text)

for ent in piano_class_doc.ents:
    print(
        f"""
{ent.text = }
{ent.start_char = }
{ent.end_char = }
{ent.label_ = }
{spacy.explain(ent.label_) = }"""
    )

displacy.serve(piano_class_doc, style="ent")
