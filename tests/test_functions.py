from app.functions import just_one_pdbpost, one_ping


def test_just_one_pdbpost():
    data = just_one_pdbpost()
    assert data == ("USA",)

def test_ping():
    data = one_ping()
    print(data["status"])
    assert data["status"] == "success"