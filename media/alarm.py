import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Laboratorium 3

        ## Symulacja alarmu przy użyciu zestawu Grove

        Zestaw Grove został opisany w poprzednim laboratorium, co ważne zasilany jest napięciem **3.3V**.

        ![Wykaz portów](https://files.seeedstudio.com/wiki/Grove_Base_Hat_for_Raspberry_Pi/img/pin-out/overview.jpg)

        ### Moduły

        W tym ćwiczeniu zostaną wykorzystane moduły czujnika ruchu oraz przycisku z diodą LED.

        Mini czujnik ruchu PIR S16-L221D pozwala wykrywać ruch w odległości do 5 metrów (rekomendowane do 2 metrów) z kątem widzenia 110 na 90 stopni. Wykorzystuje światło podczerwone. Korzysta z łącza **cyfrowego**. Współpracuje z 3.3V lub 5V.

        Przycisk z diodą komunikuje się przy użyciu łącznika **cyfrowego**. Współpracuje z dowolnym z napięć 3.3V, 5V. Przełącznik jest domyślnie ustawiony w **stan wysoki**, podpięty do **wewnętrznej linii** sygnałowej, a dioda w **stan niski** na **linii zewnętrznej**.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z1. Identyfikacja portów

        Uzupełnij poniższe zmienne numerami identyfikującymi połączenia urządzeń. Numer portu znajduje się na płytce nad portem, obok litery **D**. Numer pinu można odczytać po lewej stronie portu, a następnie użyć informacji o module do prawidłowego przypisania urządzeń.
        """
    )
    return


@app.cell
def _():
    sensor_port = 5
    led_pin = 16
    btn_pin = 17
    return btn_pin, led_pin, sensor_port


@app.cell(hide_code=True)
def _(btn_pin, led_pin, mo, sensor_port, test_z1):
    mo.md(f'Zadanie Z1. {"" if test_z1(sensor_port, led_pin, btn_pin) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Obiekty pomocnicze `motion` i `btn` pozwalają na dostęp do sensorów. Wymagają one sprecyzowania portu podłączenia w interfejsie GPIO.""")
    return


@app.cell
def _(
    GroveLEDButton,
    GroveMiniPIR,
    btn_pin,
    led_pin,
    mo,
    sensor_port,
    test_z1,
):
    mo.stop(not test_z1(sensor_port, led_pin, btn_pin), mo.md('Zadanie Z1. nie jest rozwiązane.'))

    motion = GroveMiniPIR(sensor_port)
    btn = GroveLEDButton(led_pin)
    return btn, motion


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z2. Wykrycie ruchu

        Alarm w momencie wykrycia ruchu powiadamia użytkownia włączając diodę na przycisku. Uzupełnij funkcję, wykorzystując obiekty `motion` i `btn`.

        Klasa `GroveMiniPIR` wykorzystuje mechanizm flagi, w momencie wykrycia ruchu flaga zostaje ustawiona na `True`, a odczytanie wartości flagi zmienia jej wartość na `False`. Wykorzystaj ten często używany mechanizm, aby ułatwić rozwiązanie zadania.

        Dane pomocnicze:  
        `motion.flag` - flaga wykrycia ruchu  
        `btn.led` - stan diody przycisku, można go zmieniać nadając wartość tej zmiennej
        """
    )
    return


@app.cell
def _(btn, motion):
    def motion_detected():
        if motion.flag:
            btn.led = True
    return (motion_detected,)


@app.cell(hide_code=True)
def _(mo, motion_detected, test_z2):
    mo.md(f'Zadanie Z2. {"" if test_z2(motion_detected) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z3. Wyłączenie alarmu

        Wciśnięcie przycisku przez użytkownika powinno wyłączyć alarm.

        Przycisk nie wykorzystuje mechanizmu flagi, natomiast daje dostęp do obecnego stanu wciśnięcia. 

        Dane pomocnicze:  
        `btn.pressed` - stan wciśnięcia przycisku  
        `btn.led` - stan diody przycisku, można go zmieniać nadając wartość tej zmiennej
        """
    )
    return


@app.cell
def _(btn):
    def btn_pressed():
        if btn.pressed:
            btn.led = False
    return (btn_pressed,)


@app.cell(hide_code=True)
def _(btn_pressed, mo, test_z3):
    mo.md(f'Zadanie Z3. {"" if test_z3(btn_pressed) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z4. Pętla główna

        Napisz pętlę aktualizującą diodę przycisku co 0.1 sekundy. Przetestuj działanie alarmu, następnie zmień opóźnienie na 3 sekundy i przetestuj ponownie. Jakie różnice istnieją między mechanizmem flagi a bezpośrednim odczytem stanu?

        To zadanie jest sprawdzane przez prowadzącego.

        Dane pomocnicze:  
        `motion_detected()` - aktualizacja diody przy wykryciu ruchu  
        `btn_pressed()` - aktualizacja diody przy wciśnięciu przycisku  
        `await sleep(delay: float)` - oczekiwanie przez `delay` sekund
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    stp = mo.ui.run_button(label='Uruchom')
    stp
    return (stp,)


@app.cell
async def _(
    btn_pin,
    btn_pressed,
    led_pin,
    mo,
    motion_detected,
    sensor_port,
    sleep,
    stp,
    test_z1,
    test_z2,
    test_z3,
):
    mo.stop(not test_z1(sensor_port, led_pin, btn_pin), mo.md('Zadanie Z1. nie jest rozwiązane.'))
    mo.stop(not test_z2(motion_detected), mo.md('Zadanie Z2. nie jest rozwiązane.'))
    mo.stop(not test_z3(btn_pressed), mo.md('Zadanie Z3. nie jest rozwiązane.'))
    mo.stop(not stp.value, mo.md('Wciśnij uruchom'))

    # Uzupełnij kod poniżej.
    while True:
        motion_detected()
        btn_pressed()
        await sleep(2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z5. Doszkalanie

        Zapoznaj się z kodem definiującym klasy pomocnicze użyte w zadaniach.
        """
    )
    return


@app.cell
def _(GPIO):
    # Ustawienie trybu adresacji portów GPIO.
    GPIO.setmode(GPIO.BCM)


    class GroveMiniPIR:
        def __init__(self, port: int):
            self.port = port
            self._flag = False
            # Wyczyszcznie poprzednio zdefiniowanych funkcji obsługujących zdarzenia.
            GPIO.remove_event_detect(port)
            # Przygotowanie pinu GPIO.
            GPIO.setup(port, GPIO.IN)
            GPIO.add_event_detect(port, GPIO.BOTH, self._handle)

        # Funkcja wywoływana dla uzyskania wartości atrybutu flag.
        @property
        def flag(self):
            # Zwrot obecnego stanu flagi.
            f = bool(self._flag)
            # Wyczyszczenie flagi podczas odczytu.
            self._flag = False
            return f

        def _handle(self, port: int):
            # Ustawienie flagi przy wykryciu ruchu.
            if GPIO.input(port):
                self._flag = True


    class GroveLEDButton:
        def __init__(self, port: int):
            self.port = port
            self._led = False
            self.pressed = False
            # Wyczyszcznie poprzednio zdefiniowanych funkcji obsługujących zdarzenia.
            GPIO.remove_event_detect(port + 1)
            # Przyotowanie pinu GPIO diody.
            GPIO.setup(port, GPIO.OUT)
            # Przygotowanie pinu GPIO przycisku.
            GPIO.setup(port + 1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(port + 1, GPIO.BOTH, self._handle, 100)

        @property
        def led(self):
            # Odczytanie stanu ze zmiennej.
            return self._led

        # Funkcja wywoływana dla ustalenia wartości atrybutu led.
        @led.setter
        def led(self, on: bool):
            # Zapis stanu do zmiennej.
            self._led = on
            # Ustawienie stanu diody.
            GPIO.output(self.port, on)

        def _handle(self, pin: int):
            # Zapis obecnego stanu przycisku.
            self.pressed = not GPIO.input(pin)
    return GroveLEDButton, GroveMiniPIR


@app.cell(hide_code=True)
def _():
    from inspect import signature as _sig
    from types import FunctionType as _FT
    import unittest.mock as _mock
    from asyncio import sleep
    import RPi.GPIO as GPIO
    import marimo as mo


    def test_z1(s, l, b):
        a = (5, 16, 18, 22, 24, 26)
        try:
            return all([
                s in a,
                l in a,
                s != l,
                l + 1 == b,
            ])
        except:
            return False

    def test_z2(f):
        if str(_sig(f)) != '()':
            return False
        mock = _mock.Mock(spec=[])
        fl = _mock.PropertyMock(return_value=True)
        ld = _mock.PropertyMock(return_value=False)
        type(mock).flag = fl
        type(mock).led = ld
        try:
            _FT(f.__code__, globals={'motion': mock, 'btn': mock})()
        except:
            return False
        return all([
            not len(mock.mock_calls),
            fl.mock_calls == [_mock.call()],
            ld.mock_calls == [_mock.call(True)],
        ])

    def test_z3(f):
        if str(_sig(f)) != '()':
            return False
        mock = _mock.Mock(spec=[])
        pd = _mock.PropertyMock(return_value=True)
        ld = _mock.PropertyMock(return_value=False)
        type(mock).pressed = pd
        type(mock).led = ld
        try:
            _FT(f.__code__, globals={'btn': mock})()
        except:
            return False
        return all([
            not len(mock.mock_calls),
            pd.mock_calls == [_mock.call()],
            ld.mock_calls == [_mock.call(False)],
        ])
    return GPIO, mo, sleep, test_z1, test_z2, test_z3


if __name__ == "__main__":
    app.run()
