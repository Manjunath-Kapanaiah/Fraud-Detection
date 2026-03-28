from app import detect_fraud

def test_small_transaction():
    assert detect_fraud(100) == False
