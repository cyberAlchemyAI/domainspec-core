from pipeline.nervous_system.funder_terrain.provenance import compute_input_hash, compute_record_hash

def test_record_sha256_excludes_itself():
    data = {"a": 1, "b": 2, "record_sha256": "fake_hash"}
    hash1 = compute_record_hash(data)

    data2 = {"a": 1, "b": 2, "record_sha256": "different_hash"}
    hash2 = compute_record_hash(data2)

    assert hash1 == hash2
