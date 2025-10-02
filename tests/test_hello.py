from hello import add  # because PYTHONPATH=src in Jenkinsfile

def test_add():
    assert add(2, 3) == 5
