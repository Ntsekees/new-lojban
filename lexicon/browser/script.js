
var g_lexicon = [];
//var g_selection = "All";

function is_string(v) {
    return Object.prototype.toString.call(v) === '[object String]';
}

function is_array(v) {
    return Object.prototype.toString.call(v) === '[object Array]';
}

function hget(map, field) {
	if (map === null || field === null) return "";
	if (field in map) {
		return map[field];
	} else return "";
}

function parsed_filter(filter) {
	var split_filter = filter
		.replace("\\@", "\u0091")
		.split("@")
		.map((f) => f.replace("\u0091", "@"));
	var col_filters = split_filter.slice(1);
	var map = {};
	map.any = split_filter[0].trim();
	col_filters.forEach((f) => {
		f = f + " ";
		var i = f.indexOf(" ");
		map[f.slice(0, i).trim()] = new RegExp(f.slice(i).trim());
	});
	return map;
}

function validated_by_filter(entry, filter) {
	var pf = parsed_filter(filter);
	var found = false;
	for (k in pf) {
		if (k === "") return;
		if (k === "any") {
			if (pf[k] === "") found = true;
			else {
				Object.keys(entry).forEach((gk) => {
					var v = hget(entry, gk);
					if (is_string(v)) {
						if (v.search(pf[k]) >= 0) {
							found = true;
						}
					} else if (is_array(v)) {
						for (e in v) {
							if (is_string(e) && e.search(pf[k]) >= 0) {
								found = true;
							}
						}
					}
				});
			}
		} else {
			if (pf[k] === "") {
				if (hget(entry, k) === "")
					found = true;
			} else {
				if (hget(entry, k).search(pf[k]) >= 0)
					found = true;
			}
		}
		if (!found)
			return false;
		found = false;
	}
	return true;
}

function run() {
	var filter = document.getElementById("filter-text").value;
	var html = "";
	var count = 0;
	if (filter !== "") {
		for (const entry of g_lexicon) {
			if (filter != "" && !validated_by_filter(entry, filter)) continue;
			count += 1;
			ehtml = "<summary><b style='color: #002255;'>" + entry["lemma"] + "</b>";
			ehtml += " <i style='font-size: 75%;'>" + entry["supertype"] + "</i> — ";
			ehtml += entry["eng_definition"] + "</summary>";
			ehtml += "<div class='entry-details'>{Additional datafields will go there}</span>"
			html += "<details class='entry'>\n" + ehtml + "\n</details>\n";
		}
	}
	html += "<details class='entry'></details>\n";
	document.getElementById("result-count").innerHTML = "(" + count + " results)";
	document.getElementById("results").innerHTML = html;
}

function setup_2(lexicon) {
	g_lexicon = lexicon;
	var s = "";
	Object.keys(lexicon).forEach((k) => {
		if (k !== "langdata")
			s += `<option value='${k}'>${k}</option>`;
	});
	//document.getElementById("fields-selector").innerHTML += s;
	//document.addEventListener('keydown', handle_keydown, true);
	const filter_text_input = document.getElementById('filter-text');
	filter_text_input.addEventListener('keydown', (event) => {
		if (event.key === 'Enter')
			run();
	});
	run();
}

function setup() {
	fetch('../lexicon.json')
    .then((response) => response.text())
    .then((json) => {setup_2(JSON.parse(json))});
}

setup();
 
