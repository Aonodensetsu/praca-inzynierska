import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Laboratorium 2

        ## Pomiar odległości przy użyciu zestawu Grove

        Grove to modułowy system do tworzenia prostych projektów wykorzystujących podzespoły oparte na standardowych interfejsach. Podstawowy zestaw zawiera HAT do podłączenia do płytki Raspberry Pi oraz 10 modułów. HAT oraz moduły wykorzystują zasilanie **3.3V**. HAT jest wyposażony w procesor STM32 obsługujący wiele portów widocznych na górnej części płytki. Porty mimo podobnego wyglądu obsługują różne metody komunikacji - cyfrową, analogową, I<sup>2</sup>C, PWM, UART. Istnieje ponad 60 modułów kompatybilnych z HATem zawartym w zestawie Grove.

        ![Wykaz portów](https://files.seeedstudio.com/wiki/Grove_Base_Hat_for_Raspberry_Pi/img/pin-out/overview.jpg)

        ### Moduły

        Zestaw składa się z następujących modułów, z czego dokładniej opisane zostaną te użyte w tych laboratoriach.

        Buzzer, przycisk z podświetleniem, czujnik natężenia światła, czujnik wilgotności gleby, sensor ruchu, serwo, czujnik temperatury i wilgotności, przekaźnik, ultradźwiękowy czujnik odległości, wyświetlacz LCD.

        Czujnik ultradźwiękowy działa w zakresie 3-350cm z dokładnością 1cm. Używa portu **cyfrowego**. Czujnik musi być podłączany **przy wyłączonym zasilaniu**. Jego wyjściem jest sygnał o czasie trwania proprocjonalnym do mierzonej odległości (PWM). Najlepiej sprawuje się mierząc płaskie powierzchnie większe od 0.5 metra kwadratowego.

        *dystans = <b>czas echa</b> \* prędkość dźwięku / 2*

        Wyświetlacz LCD wykorzysuje port **I<sup>2</sup>C**. Wspiera znaki łacińskie i japońskie (a więc **brak polskich liter**).
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z1. Identyfikacja wyświetlacza

        Wykorzystaj [dokumentację](https://wiki.seeedstudio.com/Grove-16x2_LCD_Series/#specification) wyświetlacza do znalezienia adresu I<sup>2</sup>C, przy użyciu którego komunikuje się to urządzenie. Użyj typu `int` w notacji szesnastkowej.
        """
    )
    return


@app.cell
def _():
    LCD_address = 0x3E
    return (LCD_address,)


@app.cell(hide_code=True)
def _(LCD_address, mo, test_z1):
    mo.md(f'Zadanie Z1. {"" if test_z1(LCD_address) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z2. Identyfikacja sensora

        Wpisz **numer** portu, do którego podłączony jest czujnik ultradźwiękowy. Jest to liczba umieszczona na płytce nad portem, obok litery D.
        """
    )
    return


@app.cell
def _():
    Sonar_port = 5
    return (Sonar_port,)


@app.cell(hide_code=True)
def _(Sonar_port, mo, test_z2):
    mo.md(f'Zadanie Z2. {"" if test_z2(Sonar_port) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z3.

        Uzupełnij zmienne tworzące instancje klas, podając odpowiednie parametry do ich konstruktorów. Pozwoli to na wykorzystanie tych urządzeń w pozostałych zadaniach.

        Sygnatury konsturktorów:  
        `GroveUltrasonicRanger(port: int)`  
        `GroveDisplay(adres: int)`
        """
    )
    return


@app.cell
def _(GroveDisplay, GroveUltrasonicRanger, LCD_address, Sonar_port):
    sonar = GroveUltrasonicRanger(Sonar_port)
    display = GroveDisplay(LCD_address)
    return display, sonar


@app.cell(hide_code=True)
def _(display, mo, sonar, test_z3):
    mo.md(f'Zadanie Z3. {"" if test_z3(sonar, display) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z4. Przetwarzanie danych

        Sensor ultradźwiękowy zwraca jedynie czas od wysłania sygnału do otrzymania echa. Uzupełnij funkcję przyjmującą czas w mikrosekundach, tak, aby zwracała odległość w centymetrach. Wykorzystaj znajomość praw fizyki (prędkość dźwięku). Pamiętaj, że fala dźwiękowa dociera do celu, odbija się, i wraca z powrotem do sensora.
        """
    )
    return


@app.cell
def time_to_dist():
    def time_to_dist(t: float) -> float:
        return t * 343 * 100 / 2 / 1000000
    return (time_to_dist,)


@app.cell(hide_code=True)
def _(mo, test_z4, time_to_dist):
    mo.md(f'Zadanie Z4. {"" if test_z4(time_to_dist) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z5. Wyświetlanie informacji

        Napisz funkcję wyświetlającą wynik pomiaru odległości na panelu LCD. Wyświetl również poprzednią wartość w drugiej linijce.

        Podpowiedź: funkcja `display.setCursor` wyznacza miejsce, gdzie umieszczona zostanie treść wiadomości.
        """
    )
    return


@app.cell
def _(display):
    def show_measurement(val: float, prev: float):
        display.setCursor(0, 0)
        display.write(f'X:   {val:6.2f} cm')
        display.setCursor(1, 0)
        display.write(f'X-1: {prev:6.2f} cm')
    return (show_measurement,)


@app.cell(hide_code=True)
def _(mo, show_measurement, test_z5):
    mo.md(f'Zadanie Z5. {"" if test_z5(show_measurement) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z6. Pętla główna

        Napisz pętlę zbierającą dane z sensora i wyświetlającą je co 1 sekundę. Pamiętaj o wyświetlaniu poprzedniej wartości. Użyj asynchronicznej funkcji uśpienia (w danych pomocniczych).

        To zadanie jest sprawdzane przez prowadzącego.

        Dane pomocnicze:  
        `sonar` - instancja klasy zbierającej dane z sensora ultradźwiękowego  
        `time_to_dist(t: float) -> float` - konwertuje czas w mikrosekundach na centymetry  
        `show_measurement(new: float, prev: float)` - wyświetla dane na ekranie  
        `await sleep(1)` - oczekuje przez 1 sekundę
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
    LCD_address,
    Sonar_port,
    display,
    mo,
    show_measurement,
    sleep,
    sonar,
    stp,
    test_z1,
    test_z2,
    test_z3,
    test_z4,
    test_z5,
    time_to_dist,
):
    mo.stop(not test_z1(LCD_address), mo.md('Zadanie Z1. nie jest rozwiązane'))
    mo.stop(not test_z2(Sonar_port), mo.md('Zadanie Z2. nie jest rozwiązane'))
    mo.stop(not test_z3(sonar, display), mo.md('Zadanie Z3. nie jest rozwiązane'))
    mo.stop(not test_z4(time_to_dist), mo.md('Zadanie Z4. nie jest rozwiązane'))
    mo.stop(not test_z5(show_measurement), mo.md('Zadanie Z5. nie jest rozwiązane'))
    mo.stop(not stp.value, mo.md('Wciśnij przycisk uruchom'))

    # uzupełnij kod poniżej
    prev = time_to_dist(sonar.get_time())
    while True:
        new = time_to_dist(sonar.get_time())
        show_measurement(new, prev)
        prev = new
        await sleep(1)
    return new, prev


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z7. Dokształcanie

        Zapoznaj się z poniższym kodem, który pokazuje jak wykorzystuje się podłączone urządzenia - definiuje pomocnicze klasy wykorzystane w zadaniach.
        """
    )
    return


@app.cell
def _():
    from grove.display.base import Display, TYPE_CHAR
    from time import time, sleep as tsleep
    from grove.gpio import GPIO
    from grove.i2c import Bus


    # Funkcja usypiająca na x mikrosekund.
    _usleep = lambda x: tsleep(x / 1000000)


    class GroveUltrasonicRanger:
        TIMEOUT_SEND = 1000
        TIMEOUT_RECV = 10000

        def __init__(self, port: int):
            # Sprawdzenie, czy wybrany jest port cyfrowy.
            if port not in (5, 16, 18, 22, 24, 26):
                raise ValueError(f'Nieprawidłowy port: {port}')
            self._pin = port
            self.dio = GPIO(port)

        def _get_time(self) -> float | None:
            # Wysłanie pulsu ultradźwiękowego.
            self.dio.dir(GPIO.OUT)
            self.dio.write(0)
            _usleep(2)
            self.dio.write(1)
            _usleep(10)
            self.dio.write(0)

            self.dio.dir(GPIO.IN)

            # Pomiar czasu referencyjnego.
            t0 = time()

            # Odebranie pulsu wysyłającego.
            count = 0
            while count < self.TIMEOUT_SEND:
                if self.dio.read():
                    break
                count += 1
            if count >= self.TIMEOUT_SEND:
                return None
            t1 = time()

            # Test, czy puls został wysłany w odpowiednim czasie od zapytania.
            if (t1 - t0) * 1000000 > 530:
                return None

            # Odebranie pulsu zwrotnego.
            count = 0
            while count < self.TIMEOUT_RECV:
                if not self.dio.read():
                    break
                count += 1
            if count >= self.TIMEOUT_RECV:
                return None
            t2 = time()

            return (t2 - t1) * 1000000

        def get_time(self) -> float:
            while True:
                t = self._get_time()
                if t:
                    return t


    class GroveDisplay(Display):
        def __init__(self, address: int):
            self._bus = Bus()
            self._addr = address
            if self._bus.write_byte(address, 0):
                raise ValueError(f'Sprawdź, czy LCD ({address}) jest podłączony')

            # Konfiguracja wyświetlacza.
            self._command(0x02)
            tsleep(0.1)
            self._command(0x08 | 0x04)
            self._command(0x28)

        @property
        def name(self) -> str:
            return 'JHD1802'

        def type(self) -> int:
            return TYPE_CHAR

        def size(self) -> tuple[int, int]:
            return 2, 16  # rows, columns

        def clear(self):
            self._command(0x01)

        def home(self):
            self._command(0x02)
            tsleep(0.2)

        def draw(self, data, bytes):
            return NotImplemented  # Niedostępne dla tego rodzaju wyświetlacza.

        def setCursor(self, row: int, column: int):
            rows, cols = self.size()
            if not all([0 <= row < rows, 0 <= column < cols]):
                raise ValueError('Poza zakresem wyświetlacza')
            self._command(0x80 + (row * 0x40) + (column % 0x10))

        def write(self, msg: str):
            for c in msg:
                self._bus.write_byte_data(self._addr, 0x40, ord(c))

        def _cursor_on(self, enable: bool):
            self._command(0x0E if enable else 0x0C)

        def _command(self, cmd: int):
            self._bus.write_byte_data(self._addr, 0x80, cmd)
    return (
        Bus,
        Display,
        GPIO,
        GroveDisplay,
        GroveUltrasonicRanger,
        TYPE_CHAR,
        time,
        tsleep,
    )


@app.cell(hide_code=True)
def _(GroveDisplay, GroveUltrasonicRanger):
    from asyncio import sleep
    import marimo as mo

    # private
    from types import FunctionType as _FT
    from random import random as _r
    from unittest.mock import Mock as _M
    from inspect import signature as _sig

    def test_z1(v):
        return v == 62

    def test_z2(v):
        return v in (5, 16, 18, 22, 24, 26)

    def test_z3(s, d):
        return all([
            isinstance(s, GroveUltrasonicRanger),
            isinstance(d, GroveDisplay)
        ])

    def test_z4(f):
        if not str(_sig(f)) == '(t: float) -> float':
            return False
        f = _FT(f.__code__, globals={})
        v = _r() * _r() * 10000
        t = v * 0.01715
        try:
            return t - 0.0001 < f(v) < t + 0.0001
        except:
            return False

    def test_z5(f):
        if not str(_sig(f)) == '(val: float, prev: float)':
            return False
        m = _M()
        try:
            _FT(f.__code__, globals={'display': m})(0, 0)
        except:
            return False
        return all([
            len(m.mock_calls) == 4,
            m.write.call_count == 2,
            m.setCursor.call_count == 2,
        ])
    return mo, sleep, test_z1, test_z2, test_z3, test_z4, test_z5


if __name__ == "__main__":
    app.run()
