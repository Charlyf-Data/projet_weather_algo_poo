import time
from projet.extractors.decorators import log_execution_time


def test_decorator_returns_correct_result():
    @log_execution_time
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5


def test_decorator_prints_messages(capsys, monkeypatch):
    # Mock du temps pour éviter les variations
    times = [1.0, 1.5]
    monkeypatch.setattr(time, "time", lambda: times.pop(0))

    @log_execution_time
    def dummy():
        return "ok"

    dummy()

    captured = capsys.readouterr()

    assert "Début de l'exécution de dummy" in captured.out
    assert "Fin de l'exécution de dummy en 0.5000 secondes" in captured.out


def test_wraps_preserves_function_name():
    @log_execution_time
    def my_function():
        pass

    assert my_function.__name__ == "my_function"
