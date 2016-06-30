from context import sample

def test_artist_search_type():
    x = 4
    assert sample.find_artist(x) == None

def test_artist_search_none():
    assert sample.find_artist("") == None

def test_artist_search_basic():
    assert sample.find_artist("Bob Dylan") == ["74ASZWbe4lXaubB36ztrGX", "Bob Dylan"]

def test_generate_artist_string_formation():
    assert sample.generate_artist_string([["dummy", "A"], ["dummy", "Comma"]]) == "A, Comma"
