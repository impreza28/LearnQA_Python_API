class TestEx10():
    def test_phrase(self):
        phrase = len(list(input("Set a phrase: "))) # посчитать длину листа из фразы
        lenPhrase = 15 #граница по условию
        assert phrase < 15, f"Фраза больше {lenPhrase} символов"

