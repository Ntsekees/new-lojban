LANG_CODES_S = """
qtq
eng cmn hin spa ara urd ben fra
ind por rus pcm arz hau swa deu
mar vie tel jpn lah amh tgl tam
tur pes apc jav yue yor wuu kor
ita pol nld bul isl eus lou
epo tok tlh qvp ithkuil-iv votgil
"""

LANG_CODES = filter(
	lambda c: c != "",
	LANG_CODES_S.replace("\n", " ").split(" ")
)
LANG_KEYS = [
	c + k
	for c in LANG_CODES
	for k in ("_definition", "_notes", "_lem", "_gloss")
]

FIELD_ORDER = (
    "lemma", "discriminator", "dialect", "supertype", "selmaho", "morphotype", "traits", "rafsis", "sememe", "tags", "examples", "synonyms", "etymology", "etymological_notes", "definition_type"
  ) + tuple(LANG_KEYS)


