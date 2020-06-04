def test_split_s3_uri():
    from prophetable.prophetable import _split_s3_uri
    S3_URI = 's3://bucket/object/key'
    PARSED_TUPLE = ('s3', 'bucket', 'object/key')
    parsed_tuple = _split_s3_uri(S3_URI)

    assert parsed_tuple == PARSED_TUPLE
