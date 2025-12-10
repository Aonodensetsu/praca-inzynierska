#!/usr/bin/env bash
#
# Metoda użycia skryptu:
# 1. Pobranie obecnej wersji ze strony Remigiusza Dończyk
#    $ wget -q https://dot.aonodensetsu.me/pi-labs.sh
# 2. Sprawdzenie kodu przed uruchomieniem na maszynie lokalnej
# 3. Umieszczenie skryptu w folderze wymienionym w zmiennej PATH
# 4. Uruchomienie skryptu po nazwie pliku
#
# Proponowane umieszczenie kopii skryptu na serwerach uniwersyteckich w celu osiągnięcia niezależności danych

set -e
if [ $EUID -ne 0 ]; then
  echo 'Uruchom skrypt jako administrator (sudo)'
  exit 1
fi
TMPDIR="$(mktemp -d)"
pushd $TMPDIR
# Utworzenie plików marimo do laboratoriów
cat >0-wprowadzenie.py <<'END'
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
        ...
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
END
cat >1-kompas.py <<'END'
import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Laboratorium 1

        ## Wykorzystanie Raspberry Pi z Sense HAT jako kompasu

        *Raspberry Pi* to mały komputer, posiadający dodatkowo interfejs pozwalający na podłączenie modułów *HAT* spełniających rozmaite funkcje, często zawierających różnego rodzaju sensory.

        *Raspberry Pi* oraz moduły są stosunkowo niedrogie, a pozwalają na projektowanie własnych urządzeń, które mogą służyć jako prototyp preprodukcyjny lub spełniać unikalną funkcję. *Raspberry Pi* jest również pełnoprawnym komputerem używającym systemu Linux, ze wzglądu na swoją wielkość bardzo przenośnym, może więc również służyć jako diagnostyczny komputer lub domowy serwer.

        W tym zadaniu do płytki podłączony jest zestaw Sense HAT, dodający możliwości pomiaru orientacji (żyroskop), przyspieszenia (akcelerometr), pola magnetycznego (magnetometr), ciśnienia atmosferycznego (barometr), temperatury (termometr) i wilgotności (higrometr). Zestaw zawiera również matrycę 8×8 pikseli oraz mały joystick.

        Aby wykorzystać sensory dostępne w urządzeniu można przeczytać ich dokumentację i użyć ich bezpośrednio, ale istnieją również pomocnicze biblioteki, które upraszczają ich wykorzystanie w kilku popularnych językach programowania - w tym przypadku w języku *Python*. Poniżej znajdują się zadania obrazujące kroki niezbędne do ich wykorzystania przy użyciu tego języka.

        ---

        ### Z1. Kalibracja IMU

        Aby użyć czujników inercyjnych (**IMU**), do których zalicza się żyroskop, akcelerometr i magnetometr, należy najpierw je skalibrować. Można to zrobić przy użyciu (już zainstalowanej) biblioteki systemowej `octave`.

        Otwórz terminal i skopiuj domyślne pliki konfiguracyjne sensora do folderu studenta:
        `cp -a /usr/share/librtimulib-utils/RTEllipsoidFit ~`

        Przejdź do skopiowanego folderu:
        `cd ~/RTEllipsoidFit`

        W tym folderze znajdują się pliki niezbędne programowi kalibracyjnemu do przetworzenia danych otrzymanych podczas kalibracji na konfigurację prawidłowo dostosowującą dane generowane w trakcie korzystania z czujników. Można dostosować te domyślne wartości dla specjalistycznych potrzeb, jednak w tym przypadku w zupełności wystarczą w niezmienionej formie.

        Aby uruchomić program kalibracyjny, użyj komendy:
        `RTIMULibCal`

        Program ten posiada prosty interfejs w języku angielskim. Wybierz opcję `m` i naciśnij dowolny przycisk, aby rozpocząć kalibrację, która odbywa się poprzez poruszanie sensorem (a zatem i płytką *Raspberry Pi*). Spróbuj obracać urządzenie w taki sposób, aby w trakcie kalibracji znalazło się w każdej możliwej orientacji. Kalibracja kończy się również poprzez naciśnięcie dowolnego przycisku.

        Wybierz opcję `x` aby wyjść z programu kalibracyjnego.

        Domyślnie plik konfiguracyjny jest zapisywany w lokalnym folderze użytkownika, jednak aby używać prawidłowej kalibracji we wszystkich programach, przenieś go w miejsce konfiguracji systemowej:
        `sudo mv ~/.config/sense_hat/RTIMULib.ini /etc`

        /// admonition
        Czujniki IMU potrzebują chwili, aby uruchomić się i skalibrować po uruchomieniu systemu. Po następnym kroku uruchamiającym system ponownie, upewnij się, że urządzenie przez 6-10 sekund po uruchomieniu (~30 sekund łącznie) nie poruszy się, aby uzyskać najdokładniejsze rezultaty.
        ///

        Po tym kroku należy zrestartować programy używające kalibracji, w tym również środowisko tego laboratorium, więc zapisz zmiany wykonane w tym pliku, a następnie użyj komendy do uruchomienia systemu ponownie:
        `sudo reboot`

        ---

        Dzięki prawidłowo skalibrowanym sensorom odczyty będą bardziej odporne na wpływ magnetyzowanych materiałów w środowisku, choć mocne zakłócenia nadal mogą spowodować błędy w odczycie informacji. Staraj się trzymać sensor z dala od urządzeń elektronicznych i elementów ferromagnetycznych w trakcie kalibracji i obsługi czujników.

        ---

        Wykorzystaj [dokumentację](https://pythonhosted.org/sense-hat/api/) API Sense HAT do prawidłowego wykonania kolejnych kroków.

        ### Z2. Konfiguracja sensorów

        Ustaw czujnik inercyjny IMU do wykorzystania żyroskopu i magnetometru, ale nie akcelerometru.
        Odpowiedzią na zadanie jest uzupełnienie funkcji wykonującej tą czynność.
        Obiekt czujnika jest dostępny jako zmienna o nazwie `sense`.
        """
    )
    return

@app.cell
def set_imu():
    def set_imu():
        ...
    return (set_imu,)


@app.cell(hide_code=True)
def _(mo, set_imu, test_z2):
    mo.md(f'Zadanie Z2. {"" if test_z2(set_imu) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z3. Zbieranie danych

        Znajdź odpowiednią funkcję w dokumentacji, aby uzyskać wartość orientacji czujnika IMU jako radiany. Wyłuskaj z rezultatu funkcji wartość `yaw`, czyli obrót wobec osi pionowej.
        """
    )
    return


@app.cell
def get_yaw():
    def get_yaw():
        ...
    return (get_yaw,)


@app.cell(hide_code=True)
def _(get_yaw, mo, test_z3):
    mo.md(f'Zadanie Z3. {"" if test_z3(get_yaw) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Z4. Wyświetl wynik na wyświetlaczu Sense. Użyj funkcji `calculate_leds(yaw_radians: float) -> list[list[int]]`, która jest już zdefiniowana. Dostępny jako parametr jest również wynik poprzedniego zadania.""")
    return


@app.cell
def draw_compass():
    def draw_compass(yaw):
        ...
    return (draw_compass,)


@app.cell(hide_code=True)
def _(draw_compass, mo, test_z4):
    mo.md(f'Zadanie Z4. {"" if test_z4(draw_compass) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    stp = mo.ui.run_button(label='Uruchom')
    stp
    return (stp,)


@app.cell
async def _(
    draw_compass,
    get_yaw,
    mo,
    set_imu,
    sleep,
    stp,
    test_z2,
    test_z3,
    test_z4,
):
    mo.stop(not test_z2(set_imu), mo.md('Zadanie 2 nie jest rozwiązane.'))
    mo.stop(not test_z3(get_yaw), mo.md('Zadanie 3 nie jest rozwiązane.'))
    mo.stop(not test_z4(draw_compass), mo.md('Zadanie 4 nie jest rozwiązane.'))
    mo.stop(not stp.value, mo.md('Wciśnij uruchom'))

    set_imu()
    while True:
        draw_compass(get_yaw())
        await sleep(0.1)
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Z5. Jakie czynniki mogą mieć wpływ na dokładność otrzymanych wyników? Poszukaj źródeł, przeprowadź dyskusję i odpowiedz na pytanie.""")
    return


@app.cell(hide_code=True)
def _():
    import sense_hat as _sense_hat
    import unittest.mock as _mock
    import inspect as _inspect
    from asyncio import sleep
    import types as _types
    import math as _math
    import marimo as mo
    import re as _re


    def calculate_leds(yaw_radians: float) -> list[list[int]]:
        center_x = 3.5
        center_y = 3.5
        leds = []
        math_angle = _math.pi / 2 - yaw_radians
        vx = _math.cos(math_angle)
        vy = _math.sin(math_angle)
        for x in range(8):
            pos_x = x - center_x
            for y in range(8):
                pos_y = center_y - y
                if abs(pos_x * vy - pos_y * vx) <= 0.5:
                    if pos_x * -vx + pos_y * -vy >= 0:
                        leds.append([150, 0, 0])
                        continue
                    leds.append([150, 150, 150])
                    continue
                leds.append([0, 0, 0])
        return leds

    def test_z2(f):
        if str(_inspect.signature(f)) != '()':
            return False
        method_mock = _mock.Mock()
        def _f(compass_enabled, gyro_enabled, accel_enabled, *args, **kwargs):
            method_mock(*args, compass_enabled=compass_enabled, gyro_enabled=gyro_enabled, accel_enabled=accel_enabled, **kwargs)
        obj_mock = _mock.Mock(set_imu_config=_f)
        try:
            _types.FunctionType(f.__code__, {'sense': obj_mock})()
        except:
            return False
        return all([
            not obj_mock.call_count,
            method_mock.mock_calls == [_mock.call(compass_enabled=True, gyro_enabled=True, accel_enabled=False)]
        ])

    def test_z3(f):
        if str(_inspect.signature(f)) != '()':
            return False
        method_mock = _mock.Mock()
        def _f(*args, **kwargs):
            method_mock(*args, **kwargs)
            return {'yaw': 0}
        obj_mock = _mock.Mock(get_orientation_radians=_f)
        try:
            _types.FunctionType(f.__code__, {'sense': obj_mock})()
        except:
            return False
        return all([
            not obj_mock.call_count,
            method_mock.mock_calls == [_mock.call()]
        ])

    def test_z4(f):
        if str(_inspect.signature(f)) != '(yaw)':
            return False
        var_mock = _mock.Mock()
        method_mock = _mock.Mock()
        def _f(*args, **kwargs):
            method_mock(*args, **kwargs)
        obj_mock = _mock.Mock(set_pixels=_f)
        try:
            _types.FunctionType(f.__code__, {'sense': obj_mock, 'calculate_leds': lambda angle: angle() and 1})(var_mock)
        except:
            return False
        return all([
            not obj_mock.call_count,
            method_mock.mock_calls == [_mock.call(1)],
            var_mock.call_count == 1
        ])

    sense = _sense_hat.SenseHat()
    sense.set_rotation(0)
    return calculate_leds, mo, sense, sleep, test_z2, test_z3, test_z4


if __name__ == "__main__":
    app.run()
END
cat >2-odleglosc.py <<'END'
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
    LCD_address = ...
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
    Sonar_port = ...
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
def _():
    sonar = ...
    display = ...
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
        return t
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

        Podpowiedzi:  
		Funkcja `display.setCursor` wyznacza miejsce, gdzie umieszczona zostanie treść wiadomości.  
        Wartość cyfrowa powinna zajmować zawsze tyle samo pól.
        """
    )
    return


@app.cell
def show_measurement():
    def show_measurement(val: float, prev: float):
        ...
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
    ...
    return


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
        t = v * 0x6B3 / 100000
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
END
cat >3-alarm.py <<'END'
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
    sensor_port = ...
    led_pin = ...
    btn_pin = ...
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
def motion_detected():
    def motion_detected():
        ...
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
def btn_pressed():
    def btn_pressed():
        ...
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
def _(
    btn_pin,
    btn_pressed,
    led_pin,
    mo,
    motion_detected,
    sensor_port,
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
END
cat >4-pogoda.py <<'END'
import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Laboratorium 4

        ## Wykorzystanie nakładki Enviro jako stacji kontroli warunków pomieszczenia

        Nakładka Enviro jest wyposażona w zestaw czujników, którego celem jest monitorowanie wnętrz pomieszczeń. Zestaw składa się z czujników wilgotności, mikrofonu, światła, zbliżeniowego, oraz wyświetlacza LCD. Dzięki pełnej integracji komponentów, nie wymaga skomplikowanej konfiguracji.

        Wykorzystany również zostanie darmowy serwis Pub/Sub `ntfy.sh` do wysłania powiadomień o niestandardowych warunkach otoczenia (w tym przypadku zakrycia czujnika zbliżeniowego).

        ---

        ### Z1. Aktualizacja sensorów

        Sensory wykorzystane w Enviro podzielone są na dwa podzespoły. `BME280` ([kod](https://github.com/pimoroni/bme280-python/blob/main/bme280/__init__.py#L247)) zawiera czujniki temperatury, ciśnienia, wilgotności, a `LTR559` ([kod](https://github.com/pimoroni/ltr559-python/blob/main/ltr559/__init__.py#L529)) czujnik zbliżeniowy oraz światła.

        Aby pobrać jakiekolwiek dane najpierw trzeba powiadomić sensor, aby zaktualizował kanały danych, gdzie dane zostaną udostępnione. W związku z brakiem dokumentacji bibliotek wyżej dostępne linki odnoszą się do miejsca w kodzie, gdzie utworzona jest funkcja o takim właśnie działaniu.

        Dostępne są obiekty `bme280` i `ltr559` reprezentujące sensory, zgodne z powyższym kodem. Uzupełnij funkcję aktualizującą dane dla obu tych sensorów. Mikrofon `sph0645lm4h_b` nie wymaga aktualizacji.
        """
    )
    return


@app.cell
def update_sensors():
    def update_sensors():
        ...
    return (update_sensors,)


@app.cell(hide_code=True)
def _(mo, test_z1, update_sensors):
    mo.md(f'Zadanie Z1. {"" if test_z1(update_sensors) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z2. Definiowanie metryk informacji

        Po aktualizacji danych dostępnych na wyjściach sensorów można zaczynać zbieranie tych dane. W celu ułatwienia tego zadania utworzony jest mechanizm pozwalający na opis informacji jako metryki. Metryki są zbiorem metainformacji opisującym w głębszy sposób zebrane dane, w tym przypadku zawierającym mechanizm zbierania informacji, nazwę wyświetlaną na ekranie, oraz jednostkę w jakiej dane są zbierane.

        Format tych metryk to: `Metric(nazwa: str, jednostka: str, funkcja_zbierająca: Callable)`.

        Poniżej znajduje się już dodana przykładowa metryka CPU (nie usuwaj jej). W podobny sposób dodaj resztę informacji na temat otoczenia. Dane będą wyświetlane na monitorze płytki, w związku z czym wykorzystaj krótkie nazwy. Wykorzystaj funkcje pomocnicze oraz obiekty `bme280`, `ltr559` oraz `sph0645lm4h_b` do uzupełnienia poniższego kodu. Zbieraj dane w sposób **pasywny** (bez wywoływania dodatkowych aktualizacji).

        **Podpowiedź:** Każda z metryk może wykorzystać funkcje jednolinijkowe lambda (nie będą za długie).

        Dostępne są funkcje pomocnicze:
        `compensate_temperature(float) -> float` - termometr znajduje się blisko procesora generującego ciepło, funkcja ta próbuje skompensować dane z sensora, aby pomiar temperatury pomieszczenia był mniej niedokładny
        `proximity_to_mm(int) -> float` - sensor zbliżeniowy zbiera dane jako wartość bezjednostkowa (2047 = blisko, 0 = daleko), funkcja ta przelicza tą wartość na milimetry (w przybliżeniu)
        """
    )
    return


@app.cell
def _(Metric, get_cpu_temperature):
    metrics = [
        Metric('CPU',   '°C',  lambda: get_cpu_temperature()),
        # dodaj linijki metryk dla temperatury, ciśnienia, wilgotności, bliskości, jasności, głośności SPL

    ]
    return (metrics,)


@app.cell(hide_code=True)
def _(metrics, mo, test_z2):
    mo.md(f'Zadanie Z2. {"" if test_z2(metrics) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ### Z3. Publikowanie danych

        Zgodnie z wcześniejszym opisem, dane będą również wysyłane przy użyciu serwisu `ntfy.sh` ([dokumentacja](https://docs.ntfy.sh/publish/#__tabbed_1_7)), co pozwoli na otrzymywanie powiadomień. Uzupełnij funkcję, aby wysłać najnowsze dane.

        Dane znajdują się w słowniku o nazwie `values`. Kluczami słownika są **nazwy metryk**. Wyślij najnowszą wartość każdej metryki. Wykorzystaj parametr `json` funkcji `requests.post` (już zaimportowanej pod nazwą `post`).

        Wysyłaj wiadomości tylko jeśli użytkownik dotyka sensora zbliżeniowego.
        """
    )
    return

@app.cell(hide_code=True)
def _(mo, ntfy_topic):
    mo.md(f'Twoja nazwa tematu: `{ntfy_topic}`.')
    return


@app.cell
def send_message():
    def send_message():
        ...
    return (send_message,)


@app.cell(hide_code=True)
def _(mo, send_message, test_z3):
    mo.md(f'Zadanie Z3 {"" if test_z3(send_message) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z4. Pętla główna

        Zbiór, przetwarzanie, wysyłanie i wyświetlanie informacji powinno być stałym procesem, który nie odbywa się jedynie jeden raz.

        Napisz pętlę główną programu, która odbywa się co sekundę. Jako opóźnienie wykorzystaj `await sleep(1)`.

        Funkcje pomocnicze:
        `await sleep(1)` - 1 sekunda opóźnienia (w trybie asynchronicznym, który jest używany w tym środowisku laboratoryjnym)
        `data_loop(list[Metric], times: int = 5) -> Metric` - jest to nieskończony iterator, która zwraca kolejne metryki po `times` razy, co pomaga w wygodnym wyświetleniu ich na ekranie
        `insert_vals(list[Metric])` - funkcja zbierająca i dopisująca wartości metryk do słownika `values`
        `display_text(Metric)` - funkcja wyświetlające na ekranie dane metryki
        `update_sensors()` - wcześniej utworzona funkcja uaktualniająca dane sensorów, pamiętaj, że pierwsze wywołanie zwraca nieprawidłowe dane
        `send_message()` - wcześniej utworzona funkcja wysyłające dane
        """
    )
    return


@app.cell
def loop():
    async def loop():
        ...
    return (loop,)


@app.cell(hide_code=True)
async def _(loop, mo, test_z4):
    mo.md(f'Zadanie Z4. {"" if await test_z4(loop) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z5. Kalibracja poziomu głośności

        Mikrofony MEMS zbierają informacje jako poziom głośności w odniesieniu do maksymalnego możliwego do odbioru, wzorując się wartością napięcia odbieranych danych. Nie jest to poziom głośności w decybelach, a tylko wartość mająca znaczenie po kalibracji otoczenia.

        Kalibracja wykorzystuje bardzo prosty wzór, do którego niezbędne są dwie wartości.

        `dbms_base` - pomiar nieskalibrowanego mikrofonu
        `spl_base` - pomiar prawdziwej głośności otoczenia w tym samym momencie

        Wykorzystaj mikrofon w swoim telefonie do pomiaru głośności pomieszczenia (np. [link](https://www.checkhearing.org/soundmeter.php)) i uzupełnij wartości funkcji, aby skalibrować odczyt płytki.

        Stan `spl_base=0, dbms_base=0` to pomiar nieskalibrowany, potrzebny do określenia prawidłowej wartości `dbms_base`.

        To zadanie nie jest sprawdzane.
        """
    )
    return


@app.cell
def _(SPH0645LM4H_B):
    sph0645lm4h_b = SPH0645LM4H_B(spl_base=0, dbms_base=0)
    return (sph0645lm4h_b,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z6. Odbieranie informacji

        Bez tworzenia konta można otworzyć stronę internetową `ntfy.sh` ([tutaj](https://ntfy.sh/app)) i zasubskrybować temat (o nazwie użytej wcześniej). Po uruchomieniu aplikacji zasłonienie czujnika zbliżeniowego spowoduje pojawienie się wiadomości w przeglądarce.

        Istnieje wiele aplikacji, które są w stanie odbierać wiadomości tego rodzaju, co pozwala wygodnie łączyć je ze sobą bez tworzenia infrastruktury.

        To zadanie jest sprawdzane przez prowadzącego.
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
    loop,
    metrics,
    mo,
    send_message,
    stp,
    test_z1,
    test_z2,
    test_z3,
    test_z4,
    update_sensors,
    values,
):
    mo.stop(not test_z1(update_sensors), mo.md('Zadanie Z1. nie jest rozwiązane.'))
    mo.stop(not test_z2(metrics), mo.md('Zadanie Z2. nie jest rozwiązane.'))
    mo.stop(not test_z3(send_message), mo.md('Zadanie Z3. nie jest rozwiązane.'))
    mo.stop(not await test_z4(loop), mo.md('Zadanie Z4. nie jest rozwiązane.'))
    mo.stop(not stp.value, mo.md('Wciśnij uruchom'))

    values.clear()
    await loop()
    return


@app.cell(hide_code=True)
def _():
    from typing import Callable, Generator, Iterator
    from matplotlib.pyplot import specgram as _sg
    from font_roboto import RobotoMedium as _RB
    from collections import deque as _deque
    from itertools import cycle as _cycle
    from threading import Lock as _Lock
    from bme280 import BME280 as _BME  # temperatura, ciśnienie, wilgotność
    from ltr559 import LTR559 as _LTR  # zbliżeniowy, światło
    from st7735 import ST7735 as _ST   # wyświetlacz
    import unittest.mock as _mock
    import PIL.ImageDraw as _ID
    import PIL.ImageFont as _IF
    import inspect as _inspect
    import sounddevice as _sd
    from asyncio import sleep
    from requests import post
    import struct as _struct
    import PIL.Image as _I
    import types as _types
    import marimo as mo
    import numpy as _np


    class SPH0645LM4H_B:
        _stream = None

        def __init__(
            self,
            *,
            sample_rate: int = 16000,
            duration: float = 1,
            spl_base: float = 0,
            dbms_base: float = 0,
        ):
            self.sample_rate = sample_rate
            self.duration = duration
            self.spl_base = spl_base
            self.dbms_base = dbms_base
            self.window_size = int(duration * sample_rate)
            self.buffer = _deque(maxlen=self.window_size)
            self._lock = _Lock()
            if self._stream is not None:
                self._stream.abort()
                self._stream.close()
            SPH0645LM4H_B._stream = _sd.RawInputStream(
                samplerate=sample_rate,
                device='adau7002',
                channels=1,
                dtype='int24',
                callback=self._callback,
                blocksize=self.window_size,
            )
            self._stream.start()

        def __del__(self):
            self._stream.abort()
            self._stream.close()
            SPH0645LM4H_B._stream = None

        def _callback(self, indata, frames, time, status):
            samples = _np.frombuffer(indata, dtype=_np.uint8).reshape(-1, 3).astype(_np.int32)
            raw = (samples[:, 2] << 16) | (samples[:, 1] << 8) | (samples[:, 0])
            raw = raw >> 6
            signed = _np.where(raw & 0x0020000, raw - 0x0040000, raw)
            norm = signed / float(2**17)
            with self._lock:
                self.buffer.extend(norm)

        def get_samples(self) -> _np.ndarray:
            with self._lock:
                return _np.array(self.buffer, dtype=_np.float32)

        def spectrogram(self) -> 'AxesImage':
            samples = self.get_samples()
            if samples.size == 0:
                samples = _np.zeros(self.window_samples)
            return _sg(samples.flatten(), Fs=self.sample_rate)[3]

        def rms(self) -> float:
            samples = self.get_samples()
            norm = samples - _np.mean(samples)
            return _np.sqrt(_np.mean(norm ** 2))

        def dbms(self) -> float:
            return 20 * _np.log10(max(self.rms(), 1e-12))

        def spl(self) -> float:
            return self.dbms() + self.spl_base - self.dbms_base


    class Metric:
        def __init__(self, name: str, unit: str, collector: Callable[[], float]):
            self.name = name
            self.unit = unit
            self.collector = collector

        def __iter__(self) -> Iterator[str | Callable[[], float]]:
            return iter((self.name, self.unit, self.collector))


    def get_cpu_temperature() -> float:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            return int(f.read()) / 1000

    def compensate_temperature(raw_temp: float, factor: float = 1.3) -> float:
        temps = values['CPU'][-5:]
        avg = sum(temps) / len(temps)
        return raw_temp - ((avg - raw_temp) / factor)

    def proximity_to_mm(val: int) -> int:
        # dopasowanie krzywej 4PL do zmierzonych danych
        return -12.56302 + 62.66476 / (1 + (val / 203.9991) ** 0.5991781)

    def insert_vals(m: list[Metric]):
        for metric in m:
            if metric.name in values:
                values[metric.name].append(metric.collector())
            else:
                values[metric.name] = [metric.collector()]
            if len(values[metric.name]) > disp.width:
                values[metric.name].pop()

    def data_loop(metrics: list[Metric], times: int = 5) -> Generator[Metric, None, None]:
        for metric in _cycle(metrics):
            for _ in range(times):
                yield metric

    def display_text(metric: Metric):
        graph_pos = font_h + 4
        bg_col = (254, 250, 244)

        vals = _np.array(values[metric.name], dtype=float)
        vmin = _np.min(vals)
        vmax = _np.max(vals)

        norm = (vals - vmin) / (vmax - vmin + 1e-6)
        line_y = disp.height - (norm * (disp.height - graph_pos))
        line_y = _np.clip(line_y, graph_pos, disp.height)

        draw.rectangle((0, 0, disp.width, disp.height), bg_col)

        n_points = len(line_y)

        x_offset = max(0, disp.width - n_points)

        for i in range(1, n_points):
            x1, y1 = x_offset + i - 1, line_y[i - 1]
            x2, y2 = x_offset + i, line_y[i]
            draw.line((x1, y1, x2, y2), fill=(0, 0, 0))

        draw.text((0, 0), f"{metric.name}: {values[metric.name][-1]:.1f} {metric.unit}", font=font, fill=(0, 0, 0))

        max_text = f"{vmax:.1f}"
        draw.rectangle(
            (0, graph_pos, draw.textlength(max_text, font=font_sm), graph_pos + font_sm_h),
            fill=bg_col
        )
        draw.text((0, graph_pos), max_text, font=font_sm, fill=(0, 0, 0))

        min_text = f"{vmin:.1f}"
        draw.rectangle(
            (0, disp.height - font_sm_h, draw.textlength(min_text, font=font_sm), disp.height),
            fill=bg_col
        )
        draw.text((0, disp.height - font_sm_h), min_text, font=font_sm, fill=(0, 0, 0))

        disp.display(img)

    def _ntfy_topic():
        import socket as _socket
        import fcntl as _fcntl
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
        info = _fcntl.ioctl(s.fileno(), 0x8927, _struct.pack('256s', bytes('eth0', 'utf-8')[:15]))
        return 'lab-' + ''.join('%02x' % b for b in info[18:24])

    def test_z1(f):
        if str(_inspect.signature(f)) != '()':
            return False
        bme_mock = _mock.Mock()
        ltr_mock = _mock.Mock()
        try:
            _types.FunctionType(f.__code__, {'bme280': bme_mock, 'ltr559': ltr_mock})()
        except:
            return False
        return all([
            bme_mock.mock_calls == [_mock.call.update_sensor()],
            ltr_mock.mock_calls == [_mock.call.update_sensor()],
        ])

    def test_z2(m):
        if len(m) != 7:
            return False
        prop_mock = _mock.PropertyMock()
        mock = _mock.Mock()
        type(mock).temperature = prop_mock
        type(mock).pressure = prop_mock
        type(mock).humidity = prop_mock
        for mtr in m:
            try:
                _types.FunctionType(mtr.collector.__code__, {
                    'bme280': mock,
                    'ltr559': mock,
                    'sph0645lm4h_b': mock,
                    'get_cpu_temperature': mock.cpu_t,
                    'get_proximity': mock.prox,
                    'proximity_to_mm': mock.prox_mm,
                    'compensate_temperature': mock.comp,
                })()
            except:
                return False
        try:
            mock.assert_has_calls([
                _mock.call.cpu_t(),
                _mock.call.comp(prop_mock()),
                _mock.call.spl(),
                _mock.call.get_proximity(passive=True),
                _mock.call.prox_mm(mock.get_proximity()),
                _mock.call.get_lux(passive=True),
            ], any_order=True)
        except AssertionError:
            return False
        return all([
            prop_mock.call_count == 4,
            len(mock.mock_calls) == 7,
        ])

    def test_z3(f):
        if str(_inspect.signature(f)) != '()':
            return False
        mock = _mock.MagicMock()
        mock.__getitem__.return_value.__getitem__.return_value = 0
        try:
            _types.FunctionType(f.__code__, {'post': mock, 'values': mock, 'ntfy_topic': 'abc'})()
        except:
            return False
        try:
            mock.assert_has_calls([
                #_mock.call.__getitem__(<PROXIMITY VALUE>),
                _mock.call.__getitem__().__getitem__(-1),
                _mock.call.items(),
                _mock.call.items().__iter__(),
                _mock.call('https://ntfy.sh/abc', json={}),
            ], any_order=True)
        except AssertionError:
            return False
        return len(mock.mock_calls) == 5

    async def test_z4(f):
        mock = _mock.Mock()
        loop_mock = _mock.Mock(return_value=[mock.metr])

        sleep_se = False
        def as_se(time, *args, **kwargs):
            nonlocal sleep_se
            if time != 1:
                raise AssertionError('Wrong sleep timing')
            if args or kwargs:
                raise AssertionError('Unknown args')
            if sleep_se:
                raise AssertionError('Slept too many times')
            else:
                sleep_se = True
        sleep_mock = _mock.AsyncMock(side_effect=as_se)

        try:
            with _mock.patch.dict(f.__globals__, {
                'metrics': mock.metr,
                'data_loop': loop_mock,
                'update_sensors': mock.upd,
                'insert_vals': mock.val,
                'send_message': mock.send,
                'display_text': mock.disp,
                'sleep': sleep_mock,
            }, clear=True):
                await f()
        except:
            return False
        return all([
            len(mock.mock_calls) == 5,
            mock.upd.call_count == 2,
            mock.send.call_count == 1,
            mock.val.mock_calls == [_mock.call(mock.metr)],
            mock.disp.mock_calls == [_mock.call(mock.metr)],
        ])


    values = {}

    # Przygotowanie wyświetlacza
    disp = _ST(
        port=0,
        cs=1,
        dc='GPIO9',
        backlight='GPIO12',
        rotation=270,
        spi_speed_hz=10000000,
    )
    img = _I.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
    draw = _ID.Draw(img)

    font_h = 20
    font_sm_h = 15
    font = _IF.truetype(_RB, font_h)
    font_sm = _IF.truetype(_RB, font_sm_h)

    ntfy_topic = _ntfy_topic()

    bme280 = _BME()
    ltr559 = _LTR()

    # Pierwszy rezultat jest nieprawidłowy
    bme280.update_sensor()
    ltr559.update_sensor()
    return (
        Callable,
        Generator,
        Iterator,
        Metric,
        SPH0645LM4H_B,
        bme280,
        compensate_temperature,
        data_loop,
        disp,
        display_text,
        draw,
        font,
        font_h,
        font_sm,
        font_sm_h,
        get_cpu_temperature,
        img,
        insert_vals,
        ltr559,
        mo,
        ntfy_topic,
        post,
        proximity_to_mm,
        sleep,
        test_z1,
        test_z2,
        test_z3,
        test_z4,
        values,
    )


if __name__ == "__main__":
    app.run()
END
cat >5-skrzyzowanie.py <<'END'
import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Laboratorium 5

        ## Wykorzystanie nakładki Traffic jako zestawu świateł.

        Nakładka ta wykorzystuje interfejs GPIO bezpośrednio, w związku z czym nie posiada oddzielnej biblioteki do kontroli świateł.

        ![hat](https://cdn3.botland.store/109065-pdt_540/traffic-phat-led-hat-for-raspberry-pi-zero-pi-supply-pis-1778.jpg)

        Diody (urządzenia **wyjściowe**) są podłączone zgodnie z **opisem** nad nimi. W związku z brakiem zewnętrznej biblioteki należy bezpośrednio ustawić porty GPIO w odpowiedni sposób, aby obsłużyć nakładkę zgodnie z poleceniami. Do prawidłowego wyboru numeru pina GPIO po jego nazwie należy posłużyć się poniższym diagramem:

        ![pinout](https://roboticsbackend.com/wp-content/uploads/2019/05/raspberry-pi-3-pinout.jpg)

        To zadanie wykorzystuje elementy poprzednich oraz zawiera fragment wykonywany w parach.

        ---

        ### Z1. Konfiguracja trybu GPIO

        Bezpośrednie użycie GPIO wymaga odpowiedniej konfiguracji złącz, czego pierwszym krokiem jest wybór trybu adresacji pinów. Tylko jeden z dostępych dwóch trybów działa niezależnie od rewizji płytki Raspberry, w związku z czym to on będzie wybrany do tego zadania.

        Informacje potrzebne do konfiguracji GPIO można znaleźć [w repozytorium](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage). Tryb, który wybieramy ma nazwę `BOARD`. Uzupełnij poniższą funkcję konfiguracją wybierającą ten tryb.
        """
    )
    return


@app.cell
def gpio_config():
    def gpio_config():
        ...
    return (gpio_config,)


@app.cell(hide_code=True)
def _(gpio_config, mo, test_z1):
    mo.md(f'Zadanie Z1. {"" if test_z1(gpio_config) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z2. Identyfikacja portów

        Porty w bibliotece przypisane są do liczb, jednak użycie bezpośrednio liczb w kodzie nie jest dobrą praktyką i może prowadzić do błędów. Znajdź odpowiednie wartości i przypisz je do zmiennych, będą one dostępne w kolejnych zadaniach.
        """
    )
    return


@app.cell
def _():
    led_red = ...
    led_yellow = ...
    led_green = ...
    return led_green, led_red, led_yellow


@app.cell(hide_code=True)
def _(led_green, led_red, led_yellow, mo, test_z2):
    mo.md(f'Zadanie Z2. {"" if test_z2(led_red, led_yellow, led_green) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z3. Konfiguracja portów

        Porty GPIO mogą zostać ustawione w tryb wejściowy lub wyjściowy. Do ich użytkowania jest niezbędna konfiguracja, domyślny jest tryb wejściowy jednak nawet użytek jako wejście **wymaga** ręcznego wyboru trybu w celu eliminacji możliwych pomyłek, jeśli na danej płytce jest utworzonych kilka programów korzystających z interfejsu GPIO.

        Uzupełnij poniższą funkcję ustawiającą odpowiednio niezbędne do tego zadania porty. Użyj zmiennych w celu uniknięcia błędów. Nie konfiguruj stanu wstępnego.
        """
    )
    return


@app.cell
def port_config():
    def port_config():
        ...
    return (port_config,)


@app.cell(hide_code=True)
def _(mo, port_config, test_z3):
    mo.md(f'Zadanie Z3. {"" if test_z3(port_config) else "nie"} jest rozwiązane.')
    return

@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z4. System świetlny

        Po skonfigurowaniu elementów GPIO mamy dostęp do użytkowania urządzenia. W związku z tematem laboratorium, niezbędne będą funkcje pokazujące odpowiednie sekwencje świetlne w celu zasymulowania działania świateł na skrzyżowaniu.

        Uzupełnij funkcje zmieniając wartość wyjściową diód w odpowiednich odstępach czasowych. Czas trwania żółtego światła to standardowo **2 sekundy**. Wykorzystaj dokumentację GPIO do ustawienia diód na włączone lub wyłączone w odpowiednim momencie. Użyj systemu czterofazowego:

        ![phases](https://upload.wikimedia.org/wikipedia/commons/f/f8/Traffic_lights_4_states.png)

        Funkcja `red_to_green` rozpoczyna się w fazie 1, a ma przejść przez fazę 2 i skończyć w fazie 3. Funkcja `green_to_red` rozpoczyna się w fazie 3, a ma przejść przez fazę 4 i skończyć w fazie 1.

        Test poprawności działania sprawdza stan świateł w momencie oczekania `asyncio.sleep` oraz na końcu funkcji. Te dwa momenty powinny zgadzać się z kolejnymi fazami systemu czterofazowego. Opóźnienie powinno wynosić standardowe 2 sekundy.
        """
    )
    return


@app.cell
def _():
    async def red_to_green():
        ...

    async def green_to_red():
        ...
    return green_to_red, red_to_green


@app.cell(hide_code=True)
async def _(green_to_red, mo, red_to_green, test_z4):
    mo.md(f'Zadanie Z4. {"" if await test_z4(red_to_green, green_to_red) else "nie"} jest rozwiązane.')
    return


@app.cell(hide_code=True)
def _(mo, ntfy_topic):
    mo.md(f"""
    ### Z5. Wysyłanie wiadomości

    Dana płytka ma zamocowane tylko jedno świało. W związku z tym do przetestowania systemu sygnalizacji będzie potrzebna praca w parach, jednak można najpierw skonfigurować i przetestować komunikację przy wykorzystaniu jednego światła. Do komunikacji podobnie jak w poprzednim laboratorium użyty zostanie serwis `ntfy.sh` ([dokumentacja](https://docs.ntfy.sh/publish/#__tabbed_1_7)).

    Nazwa twojego kanału to: `{ntfy_topic}`. W kodzie dostępna jest zmienna `ntfy_topic`, która ją przechowuje.

    W celu zaliczenia zadania usuń znak komentarza (#) z poniższej linijki i po uruchomieniu kodu odbierz wiadomość o treści 'zaliczono'. Wiadomość wyślij z terminala przy użyciu `curl`.
    """)
    return


@app.cell
def _():
    #receive_task(duration=30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Z6. Skrzyżowanie

        To zadanie będzie wymagało testowania przy użyciu dwóch płytek. Jedna przyjmie rolę nadrzędnej i będzie wysyłać wiadomości na swój kanał, a druga podrzędnej i będzie słuchać wiadomości **na kanale pierwszej**. Wiadomości powinny informować podrzędną płytkę kiedy wywoływać funkcje `red_to_green` i `green_to_red`.

        Domyślny stan diód to światło zielone dla płytki nadrzędnej i czerwone dla płytki podrzędnej.

        Funkcja odbierająca **musi** obsługiwać wiadomość **zakańczającą pętlę**, a funkcja wysyłająca **nie może** być nieskończona, aby ułatwić sprawdzanie zadania.

        Uzupełnij funkcje wykonujące obie z tych ról wspomagając się dokumentacją `ntfy.sh`. Następnie wybierz drugą osobę, z którą przetestujesz odpowiedź. Po przetestowaniu zamieńcie role płytek, przetestujcie drugą część zadania i zgłoście zakończenie ćwiczenia.

        **Podpowiedź:** Obie części wymagają uruchomienia w pętli, która w przypadku płytki podrzędnej będzie stale nasłuchiwać i obsługiwać otrzymane wiadomości, a w przypadku płytki nadrzędnej w odpowiednich momentach wysyłać komunikaty i zmieniać stan własny, aby sygnalizacja była zsynchronizowana. Pamiętaj, że światło zielone ani żółte nie może się pojawić na obu światłach jednocześnie.
        """
    )
    return


@app.cell
def _():
    async def sender():
        ...

    async def receiver():
        ...
    return receiver, sender


@app.cell(hide_code=True)
def _(mo):
    role = mo.ui.checkbox(label="Ta płytka jest nadrzędna", value=True)
    enabled = mo.ui.run_button(label="Uruchom komunikację")
    mo.hstack([enabled, role])
    return enabled, role


@app.cell(hide_code=True)
async def _(
    GPIO,
    enabled,
    gpio_config,
    green_to_red,
    led_green,
    led_red,
    led_yellow,
    mo,
    port_config,
    receiver,
    red_to_green,
    role,
    sender,
    test_z1,
    test_z2,
    test_z3,
    test_z4,
    test_z5,
):
    mo.stop(not test_z1(gpio_config), mo.md('Zadanie Z1. nie jest rozwiązane.'))
    mo.stop(not test_z2(led_red, led_yellow, led_green), mo.md('Zadanie Z2. nie jest rozwiązane.'))
    mo.stop(not test_z3(port_config), mo.md('Zadanie Z3. nie jest rozwiązane.'))
    mo.stop(not await test_z4(red_to_green, green_to_red), mo.md('Zadanie Z4. nie jest rozwiązane.'))
    mo.stop(not test_z5(), mo.md('"Zadanie Z5. nie jest rozwiązane.'))
    mo.stop(not enabled.value, mo.md('Wciśnij uruchom'))

    gpio_config()
    port_config()

    # stan początkowy
    GPIO.output(led_green if role.value else led_red, GPIO.HIGH)

    # pętla
    await (sender if role.value else receiver)()

    # wyczyszczenie stanu GPIO
    GPIO.cleanup()
    return


@app.cell(hide_code=True)
def _(ntfy_task_completed):
    import unittest.mock as _mock
    import requests as _requests
    import inspect as _inspect
    from asyncio import sleep
    import socket as _socket
    import struct as _struct
    import RPi.GPIO as GPIO
    import fcntl as _fcntl
    import types as _types
    import json as _json
    import marimo as mo


    ntfy_task_completed = False

    def _ntfy_topic():
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
        info = _fcntl.ioctl(s.fileno(), 0x8927, _struct.pack('256s', bytes('eth0', 'utf-8')[:15]))
        return 'lab-' + ''.join('%02x' % b for b in info[18:24])

    ntfy_topic = _ntfy_topic()

    def receive_task(duration=10):
        global ntfy_task_completed
        if ntfy_task_completed:
            return mo.md('Zadanie Z5. jest rozwiązane.')
        resp = _requests.get(f"https://ntfy.sh/{ntfy_topic}/json", stream=True, timeout=duration)
        for line in resp.iter_lines():
            if line:
                try:
                    j = _json.loads(line)
                    if j['message'] == 'zaliczono':
                        ntfy_task_completed = True
                        return mo.md('Zadanie Z5. jest rozwiązane.')
                except:
                    pass
                print(j)

    def test_z1(f):
        if str(_inspect.signature(f)) != '()':
            return False
        obj_mock = _mock.Mock(spec=['setmode', 'BOARD'])
        try:
            _types.FunctionType(f.__code__, {'GPIO': obj_mock})()
        except:
            return False
        return obj_mock.mock_calls == [_mock.call.setmode(obj_mock.BOARD)]

    def test_z2(led_red, led_yellow, led_green):
        return all([
            led_red == 16,
            led_yellow == 18,
            led_green == 22
        ])

    def test_z3(f):
        if str(_inspect.signature(f)) != '()':
            return False
        obj_mock = _mock.Mock(spec=['setup', 'OUT'])
        try:
            _types.FunctionType(f.__code__, {'GPIO': obj_mock, 'led_red': 16, 'led_yellow': 18, 'led_green': 22})()
        except:
            return False
        try:
            match len(obj_mock.mock_calls):
                case 1:
                    return (
                        set(obj_mock.setup.call_args[0][0]) == {16, 18, 22}
                        and obj_mock.setup.call_args[0][1] == obj_mock.OUT
                    )
                case 3:
                    obj_mock.setup.assert_has_calls([
                        _mock.call(16, obj_mock.OUT),
                        _mock.call(18, obj_mock.OUT),
                        _mock.call(22, obj_mock.OUT)
                    ], any_order=True)
                    return True
        except AssertionError:
            return False

    async def test_z4(rg, gr):
        if str(_inspect.signature(rg)) != '()':
            return False
        if str(_inspect.signature(gr)) != '()':
            return False
        storage = {
            'rg': [],
            'gr': [],
            't': []
        }
        gpio_rg_mock = _mock.Mock(spec=['output', 'HIGH', 'LOW'])
        gpio_gr_mock = _mock.Mock(spec=['output', 'HIGH', 'LOW'])
        # kiedy wywołany jest sleep stan diód powinien być zgodny z kolejną fazą świateł
        # zapisuję te fazy aby później sprawdzić poprawność działania
        asyncio_rg_mock = _mock.AsyncMock(
            spec=[],
            side_effect=lambda t: storage['t'].append(t) or storage['rg'].append([
                (x[0][0], x[0][1]._extract_mock_name()) for x in gpio_rg_mock.output.call_args_list
            ])
        )
        asyncio_gr_mock = _mock.AsyncMock(
            spec=[],
            side_effect=lambda t: storage['t'].append(t) or storage['gr'].append([
                (x[0][0], x[0][1]._extract_mock_name()) for x in gpio_gr_mock.output.call_args_list
            ])
        )
        common = {'led_red': 16, 'led_yellow': 18, 'led_green': 22}
        try:
            with _mock.patch.dict(rg.__globals__, {**common, 'GPIO': gpio_rg_mock, 'sleep': asyncio_rg_mock}, clear=True):
                await rg()
            with _mock.patch.dict(gr.__globals__, {**common, 'GPIO': gpio_gr_mock, 'sleep': asyncio_gr_mock}, clear=True):
                await gr()
        except:
            return False
        # ilość uruchomień komend
        if any([
            len(asyncio_gr_mock.mock_calls) != len(asyncio_rg_mock.mock_calls),
            len(asyncio_gr_mock.mock_calls) != 1,
            len(gpio_gr_mock.mock_calls) != len(gpio_rg_mock.mock_calls),
            len(gpio_gr_mock.mock_calls) != 4,
        ]):
            return False
        # standardowe opóźnienie 2 sekundy
        if not all(x == 2 for x in storage['t']):
            return False
        # faza 1->2
        state = {16: 'mock.HIGH', 18: 'mock.LOW', 22: 'mock.LOW'}
        for call in storage['rg'][0]:
            state[call[0]] = call[1]
        if state != {16: 'mock.HIGH', 18: 'mock.HIGH', 22: 'mock.LOW'}:
            return False
        # faza 2->3
        for call in gpio_rg_mock.output.call_args_list:
            state[call[0][0]] = call[0][1]._extract_mock_name()
        if state != {16: 'mock.LOW', 18: 'mock.LOW', 22: 'mock.HIGH'}:
            return False
        # faza 3->4
        for call in storage['gr'][0]:
            state[call[0]] = call[1]
        if state != {16: 'mock.LOW', 18: 'mock.HIGH', 22: 'mock.LOW'}:
            return False
        # faza 4->1
        for call in gpio_gr_mock.output.call_args_list:
            state[call[0][0]] = call[0][1]._extract_mock_name()
        if state != {16: 'mock.HIGH', 18: 'mock.LOW', 22: 'mock.LOW'}:
            return False
        return True

    def test_z5():
        global ntfy_task_completed
        return ntfy_task_completed
    return (
        GPIO,
        mo,
        ntfy_task_completed,
        ntfy_topic,
        receive_task,
        sleep,
        test_z1,
        test_z2,
        test_z3,
        test_z4,
        test_z5,
    )


if __name__ == "__main__":
    app.run()
END
# Przygotowanie folderu środowiska
install -m 755 -o student -g student -d /home/student/Workspace
install -m 644 -o student -g student -t /home/student/Workspace/ 0-wprowadzenie.py 1-kompas.py 2-odleglosc.py 3-alarm.py 4-pogoda.py 5-skrzyzowanie.py
# Instalacja zależności
cat >requirements.txt <<'END'
ads1015==1.0.0
aiohappyeyeballs==2.6.1
aiohttp==3.13.0
aiosignal==1.4.0
altair==5.5.0
anyio==4.9.0
arro3-core==0.4.6
astral==3.2
asyncio==4.0.0
attrs==25.3.0
certifi==2025.10.5
cffi==2.0.0
charset-normalizer==3.4.3
click==8.1.8
docutils==0.21.2
duckdb==1.2.1
enviroplus==1.0.2
font-roboto==0.0.1
fonts==0.0.3
frozenlist==1.8.0
gpiod==2.3.0
gpiodevice==0.0.5
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
i2cdevice==1.0.0
idna==3.10
itsdangerous==2.2.0
jedi==0.19.2
Jinja2==3.1.6
jsonschema==4.23.0
jsonschema-specifications==2024.10.1
ltr559==1.0.0
marimo==0.11.31
Markdown==3.7
MarkupSafe==3.0.2
matplotlib==3.10.7
multidict==6.7.0
narwhals==1.32.0
numpy==2.2.4
packaging==24.2
paho-mqtt==2.1.0
parso==0.8.4
pillow==11.1.0
pimoroni-bme280==1.0.0
pms5003==1.0.1
polars==1.26.0
propcache==0.4.1
psutil==7.0.0
pyarrow==19.0.1
pycparser==2.23
pycrdt==0.11.1
Pygments==2.19.1
pymdown-extensions==10.14.3
pyserial==3.5
pysocks==1.7.1
pytz==2025.2
PyYAML==6.0.2
referencing==0.36.2
requests==2.32.5
rpds-py==0.24.0
rpi-lgpio==0.6
RTIMULib @ git+https://github.com/RPi-Distro/RTIMULib@b949681af69b45f0f7f4bb53b6770037b5b02178#subdirectory=Linux/python
ruff==0.11.2
Seeed-grove.py @ git+https://github.com/Seeed-Studio/grove.py.git@614734d1ed73e512439185484d19e787dea7cc87
sense-hat==2.6.0
smbus==1.1.post2
smbus2==0.4.2
sniffio==1.3.1
sounddevice==0.5.2
spidev==3.8
sqlglot==26.12.0
st7735==1.0.0
starlette==0.46.1
tomlkit==0.13.2
typing_extensions==4.13.0
urllib3==2.5.0
uvicorn==0.34.0
vegafusion==2.0.2
vl-convert-python==1.7.0
websockets==15.0.1
yarl==1.22.0
END
cat >marimo.toml <<'END'
[language_servers.pylsp]
enable_ruff = true
enable_mypy = true
enable_pylint = false
enabled = true
enable_pyflakes = false
enable_pydocstyle = false
enable_flake8 = false

[ai]
rules = ""

[experimental]

[display]
theme = "dark"
code_editor_font_size = 14
dataframes = "rich"
cell_output = "above"
default_width = "medium"

[completion]
activate_on_typing = true
copilot = false

[save]
autosave_delay = 1000
autosave = "after_delay"
format_on_save = false

[keymap]
preset = "default"

[keymap.overrides]

[package_management]
manager = "pip"

[server]
follow_symlink = false
browser = "default"

[formatting]
line_length = 79

[snippets]
custom_paths = []
include_default_snippets = true

[runtime]
watcher_on_save = "lazy"
std_stream_max_bytes = 1000000
on_cell_change = "autorun"
pythonpath = []
auto_instantiate = true
output_max_bytes = 8000000
auto_reload = "autorun"
END
chmod 755 .
chmod 777 requirements.txt
install -m 755 -o student -g student -d /home/student/.config/marimo
install -m 644 -o student -g student marimo.toml /home/student/.config/marimo/
# Ustawienia systemowe
nmcli con mod preconfigured wifi.powersave disable
raspi-config nonint do_i2c 0
raspi-config nonint do_spi 0
grep -Fxq 'dtoverlay=adau7002-simple' /boot/firmware/config.txt || sed -i '1i dtoverlay=adau7002-simple' /boot/firmware/config.txt
grep -Fxq 'dtparam=i2s=on' /boot/firmware/config.txt || sed -i '1i dtparam=i2s=on' /boot/firmware/config.txt
apt update
apt install -y python3 python3-venv pyenv git libopenjp2-7 octave
if [ ! -d /home/student/.pyenv/versions/3.11.11 ]; then
  su student -c 'cd ~; pyenv install 3.11.11'
  setcap CAP_NET_BIND_SERVICE=+eip /home/student/.pyenv/versions/3.11.11/bin/python3.11
fi
if [ ! -d /home/student/.venv ]; then
  su student -c '~/.pyenv/versions/3.11.11/bin/python3 -m venv ~/.venv && ~/.venv/bin/pip install -U pip==25.0.1 && ~/.venv/bin/pip install -r requirements.txt'
fi
# Uruchomienie środowiska przy włączeniu systemu
cat >pi-labs-workspace.service <<'END'
[Unit]
Description=Srodowisko Laboratoriow Raspberry Pi
After=multi-user.target

[Service]
User=student
Group=student
Type=simple
Restart=always
RestartSec=5
WorkingDirectory=/home/student/Workspace
ExecStart=/home/student/.venv/bin/marimo edit --host 127.0.0.1 --port 80 --headless --skip-update-check --no-token

[Install]
WantedBy=multi-user.target
END
install -m 755 pi-labs-workspace.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable pi-labs-workspace
# Czyszczenie dodatkowych plików po poprzednich laboratoriach
if [ -d /home/student/RTEllipsoidFit ]; then rm -rf /home/student/RTEllipsoidFit; fi
if [ -d /home/student/.config/sense_hat ]; then rm -rf /home/student/.config/sense_hat; fi
if [ -f /etc/RTIMULib.ini ]; then rm /etc/RTIMULib.ini; fi
# Ikona na pulpicie
cat >Environment.desktop <<'END'
[Desktop Entry]
Type=Link
URL=http://localhost
Name=Środowisko Laboratoryjne
Icon=firefox-esr
END
install -m 755 Environment.desktop /home/student/Desktop/
# Niestety niezbędne z powodu zmian konfiguracji urządzeń
reboot
