from scripts.audit_clinical_gaps import KB_ROOT, audit


def test_drug_indication_gap_reports_modelled_and_unmodelled_pairs():
    report = audit(KB_ROOT)
    metric = next(item for item in report["gaps"] if item["id"] == "drug_indication_tracking")

    details = metric["details"]
    assert metric["status"] == "coverage_gap"
    assert details["drug_indications_entity_dir_present"] is True
    assert details["drug_indication_records"] >= 1
    assert details["source_backed_assessed_pairs"] >= 1
    assert details["missing_explicit_pair_count"] > 0


def test_modality_gap_counts_current_first_class_entities():
    report = audit(KB_ROOT)
    metric = next(item for item in report["gaps"] if item["id"] == "surgery_radiation_structure")

    details = metric["details"]
    assert metric["status"] == "coverage_gap"
    assert details["has_structured_procedures"] is True
    assert details["has_structured_radiation_courses"] is True
    assert details["structured_procedure_count"] >= 1
    assert details["structured_radiation_course_count"] >= 1
