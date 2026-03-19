def test_importing_north_tool():
    # this will raise an exception if pydantic model validation fails
    from swe_module.north_tools import north_entry_point

    expected_id = 'swe-module-swe-north-tool'
    assert (
        north_entry_point.id_url_safe == expected_id
        or north_entry_point.id == 'nomad-north-swe_norm'
    ), 'NORTHTool entry point has incorrect id or id_url_safe'
