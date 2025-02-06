from app.functions import just_one_pdbpost

def test_just_one_pdbpost():
    data = just_one_pdbpost()
    assert data == ("USA",)