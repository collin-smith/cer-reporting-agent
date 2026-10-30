"""fetch_cer: encoding, schema checks, snapshot diff and operator grouping. All names are fictional."""

import fetch_cer as f


def test_cp1252_is_detected_when_utf8_fails():
    assert f.detect_encoding("Trans Québec".encode("cp1252")) == "cp1252"
    assert f.detect_encoding("Trans Québec".encode()) == "utf-8"
    assert f.detect_encoding(b"\xef\xbb\xbfA,B\n") == "utf-8-sig"


def test_schema_check_flags_missing_required_and_header_changes():
    header = ["Incident Number", "Company", "Status"]
    errors = f.check_schema(header, previous=["Incident Number", "Company", "Province"], required=["Incident Number"])
    assert "column removed or renamed since last snapshot: 'Province'" in errors
    assert "new column since last snapshot: 'Status'" in errors
    assert f.check_schema(header, previous=header, required=["Rupture"]) == ["required column missing: 'Rupture'"]


def test_dictionary_gaps_ignore_case_and_whitespace():
    csv_only, dict_only = f.dictionary_gaps(["Weld type ", "Rupture"], ["weld  type", "Released substance"])
    assert csv_only == ["rupture"]
    assert dict_only == ["released substance"]


def test_diff_reports_new_removed_and_changed_fields():
    before = [{"Incident Number": "A", "Status": "Submitted"}, {"Incident Number": "B", "Status": "Closed"}]
    after = [{"Incident Number": "A", "Status": "Closed"}, {"Incident Number": "C", "Status": "Initially Submitted"}]
    d = f.diff(before, after)
    assert d["new"] == ["C"] and d["removed"] == ["B"] and d["changed"] == ["A"]
    assert d["changed_fields"]["Status"] == 1


def test_operator_key_drops_suffixes_and_partnership_clauses():
    assert f.operator_key("Prairie Midstream Ltd.") == "prairie midstream"
    assert f.operator_key("Prairie Midstream Limited") == "prairie midstream"
    assert (
        f.operator_key("Aspen Ridge GP Ltd., as general partner on behalf of Aspen Ridge Limited Partnership")
        == "aspen ridge"
    )
    assert f.operator_key("Northline Gas Inc., carrying on business as Northline Transmission") == "northline gas"


def test_operator_map_groups_variants_and_applies_overrides():
    counts = {"Prairie Midstream Ltd.": 5, "Prairie Midstream Limited": 1, "Aspen Ridge GP Ltd.": 3,
              "Northline Gas Inc.": 9}  # fmt: skip
    m = f.build_operator_map(counts, overrides={"aspen ridge": "northline gas"})
    assert m["Prairie Midstream Limited"] == ("Prairie Midstream Ltd.", "grouped")
    assert m["Aspen Ridge GP Ltd."] == ("Northline Gas Inc.", "override")
    assert m["Northline Gas Inc."] == ("Northline Gas Inc.", "as-is")
