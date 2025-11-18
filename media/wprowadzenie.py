import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Wprowadzenie

        ### Czym jest marimo?

        Te laboratoria z Raspberry Pi są utworzone przy użyciu środowiska `marimo`. Marimo to program pozwalający na tworzenie interaktywnych notatników w języku `Python`. Marimo posiada pewne cechy, które zostaną wyjaśnione w tym wprowadzeniu w celu ułatwienia wykonywania zadań.

        ### Kod notatnika

        Definiowany jest w komórkach:
        """
    )
    return


@app.cell
def _():
    a = 1 + 2
    return (a,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Ten tekst informacyjny również znajduje się w specjalnym rodzaju komórki do tekstu.

        Wynik ostatniej linijki komórki jest również wyświetlany jako wyjście:
        """
    )
    return


@app.cell
def _():
    1 + 2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Kod komórki może również być ukryty. W ten sposób będzie definiowany kod pomagający w wykonaniu zadań.""")
    return


@app.cell(hide_code=True)
def _():
    b = 'Kod jest wyszarzony i wyświetla się jedynie jedna linijka, a reszta jest ukryta'
    return (b,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Informacje wypisywane przez kod wyświetlane są poniżej:""")
    return


@app.cell
def _():
    print('tutaj')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Błędy również są dobrze widoczne, wykorzystują zarówno konsolę jak i obszar wyjściowy:""")
    return


@app.cell
def _():
    raise ValueError()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Uzupełnianie danych

        Jako treść zadań, pojawią się komórki z niedokończonym kodem używającym trzy kropki `...`. Te miejsca należy uzupełnić zgodnie z poleceniem, pod większością z tych komórek będzie komórka sprawdzająca rozwiązanie zadania.

        Uzupełnij poniższą funkcję sformułowaniem `return v`.
        """
    )
    return


@app.cell
def example():
    def example(v):
        return v
    return (example,)


@app.cell(hide_code=True)
def _(example, mo, test_example):
    mo.md(f'Zadanie przykładowe {"" if test_example(example) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Komórki mogą również wymagać uzupełnienia wcześniejszych komórek. Jest to używane najczęściej w finalnej komórce składającej wszystkie elementy ćwiczenia w działający program.""")
    return


@app.cell
def _(a, example, mo, test_example):
    mo.stop(not test_example(example), mo.md('Zadanie przykładowe nie jest rozwiązane.'))
    a  # = 3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Asynchroniczność

        Marimo jest środowiskiem asynchronicznym, w związku z czym w niektórych miejscach mogą pojawić się słowa kluczowe `async` i `await`. W ćwiczeniach często pojawiać się będą dwa asynchroniczne sformułowania.

        - `async def` w przeciwieństwie do `def` tworzy funkcję asynchroniczną, opcja ta będzie używana w kilku miejscach do utworzenia funkcji, które mogą wykorzystywać inne funkcje asynchroniczne  
          aby uruchomić funkcje asynchroniczne należy oczekiwać na ich rezultat przy użyciu słówka `await`
        - `asyncio.sleep` to asynchroniczny odpowiednik `time.sleep`, który na określony czas uśpi kod, jednak nie usypiając również całego środowiska marimo - będzie używany wszędzie tam, gdzie poza notatnikiem pojawiłoby się `time.sleep`

        ```python
        def funkcja_synchroniczna():
            # nie można wywołać funkcji asynchronicznej ze zwykłej funkcji
            await asyncio.sleep(1)  # BŁĄD

        async def funkcja_asynchroniczna():
            # w laboratoriach asyncio.sleep będzie zaimportowane pod nazwą sleep
            await sleep(1)

        # użycie funkcji zdefiniowanej przez nas również wymaga słówka await
        await funkcja_asynchroniczna()
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Ostatnia ukryta komórka definiuje większość kodu pomocniczego do zadań, nie należy zmieniać jej zawartości.""")
    return


@app.cell(hide_code=True)
def _():
    from inspect import signature as _sig
    from types import FunctionType as _FT
    import marimo as mo

    def test_example(f):
        if str(_sig(f)) != '(v)':
            return False
        fc = _FT(f.__code__, globals={})
        try:
           return all([
               fc(15) == 15,
               fc('3') == '3',
               fc(True) is True,
           ])
        except:
            return False
    return mo, test_example


if __name__ == "__main__":
    app.run()
