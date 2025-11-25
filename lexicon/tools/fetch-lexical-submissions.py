
# ============================================================ #

import sys, os, time

from common import table_from_csv_url, object_from_json_path, save_as_json_file

SELF_PATH = os.path.dirname(os.path.realpath(__file__))

# ============================================================ #

FORM_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1C-xhzaMuslBr5G4PNShpvmEWi37e1jP1O0XkNkPcQWM/gviz/tq?tqx=out:csv&sheet=Form Responses 1"

def entrypoint():
	start_time = time.time()
	def normalized(path):
		return path.replace("/", os.path.sep)
	lexicon_path = SELF_PATH + normalized("/../lexicon.json")
	data = object_from_json_path(lexicon_path)
	try:
		submissions = table_from_csv_url(FORM_SHEET_CSV_URL)
	except:
		print(
			f"Unexpected error upon fetching the lexical submissions: {str(sys.exc_info()[0])}")
		sys.exit()
	data = with_added_submissions(data, submissions)
	save_as_json_file(data, lexicon_path)
	print("Execution time: {:.3f}s.".format(
		time.time() - start_time))

def with_added_submissions(data, submissions):
	if len(submissions) > 1:
		header, body = submissions[0], submissions[1 :]
		submissions = [as_map(row, header) for row in body]
	data_lemmas = [ e["lemma"] for e in data]
	for s in submissions:
		if s["lemma"] in data_lemmas:
			print(f"⚠⚠⚠ Lemma ⟪{s['lemma']}⟫ is already in the lexicon!")
		else:
			data_lemmas.append(s["lemma"])
			data.append(s)
	return data

def as_map(row, header):
	def checked_nonempty(s):
		if s == "":
			print(f"⚠⚠⚠ INVALID ENTRY FOR LEMMA ⟪{row[1]}⟫!")
		return s
	return {
		"lemma": checked_nonempty(row[1]),
		"discriminator": "",
		"dialect": "",
		"supertype": "",
		"selmaho":  checked_nonempty(row[2]).upper().replace("'", "h"),
		"morphotype": "",
		"traits": "",
		"rafsis": row[4],
		"sememe": "",
		"examples": [],
		"synonyms": "",
		"etymology": "",
		"eng_etymological_notes": row[3],
		"eng_definition": with_adjusted_slot_notation(checked_nonempty(row[5])),
		"eng_notes": row[6]
	}

def with_adjusted_slot_notation(s):
	circled = "🄌➊➋➌➍➎➏➐➑➒"
	for n in range(1, 9):
		bracket_notation = "[" + str(n) + "]"
		s = s.replace(bracket_notation, circled[n])
	return s

# ============================================================ #

# === ENTRY POINT === #

entrypoint()


