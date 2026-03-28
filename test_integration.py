from app import detect_fraud

def test_large_transaction():
    assert detect_fraud(20000) == True
