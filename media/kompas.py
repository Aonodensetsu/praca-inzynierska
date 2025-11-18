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
        Moduł *Sense HAT* zawiera wyświetlacz kolorowy 8×8, mały joystick, oraz czujniki: żyroskop, akcelerometr, magnetometr, termometr, higrometr, ciśnieniomierz, czujnik naświetlenia.

        *Raspberry Pi* oraz moduły są stosunkowo niedrogie, a pozwalają na projektowanie własnych urządzeń, które mogą służyć jako prototyp preprodukcyjny lub spełniać unikalną funkcję. *Raspberry Pi* jest również pełnoprawnym komputerem używającym systemu Linux, ze wzglądu na swoją wielkość bardzo przenośnym, może więc również służyć jako diagnostyczny komputer lub domowy serwer.

        W tym zadaniu do płytki podłączony jest zestaw Sense HAT, dodający możliwości pomiaru orientacji (żyroskop), przyspieszenia (akcelerometr), pola magnetycznego (magnetometr), ciśnienia atmosferycznego (barometr), temperatury (termometr) i wilgotności (higrometr). Zestaw zawiera również matrycę 8×8 pikseli oraz mały joystick.

        Aby wykorzystać sensory dostępne w urządzeniu można przeczytać ich dokumentację i użyć ich bezpośrednio, ale istnieją również pomocnicze biblioteki, które upraszczają ich wykorzystanie w kilku popularnych językach programowania - w tym przypadku w języku *Python*. Poniżej znajdują się zadania obrazujące kroki niezbędne do ich wykorzystania przy użyciu tego języka.

        ---

        ### Z1. Kalibracja IMU

        Aby użyć czujników inercyjnych (**IMU**), do których zalicza się żyroskop, akcelerometr i magenetometr, należy najpierw je skalibrować. Można to zrobić przy użyciu (zainstalowanej) biblioteki systemowej `octave`.

        Otwórz terminal i skopiuj domyślne pliki konfiguracyjne sensora do folderu studenta:
        `cp -a /usr/share/librtimulib-utils/RTEllipsoidFit ~`

        Przejdź do skopiowanego folderu:
        `cd RTEllipsoidFit`

        W tym folderze znajdują się pliki niezbędne programowi kalibracyjnemu do przetworzenia danych otrzymanych podczas kalibracji na konfigurację prawidłowo dostosowującą dane w trakcie korzystania z czujników. Można dostosować te domyślne wartości do specjalistycznych potrzeb, jednak w tym przypadku w zupełności wystarczą w niezmienionej formie.

        Aby uruchomić program kalibracyjny, użyj komendy:
        `RTIMULibCal`

        Program ten posiada prosty interfejs w języku angielskim. Wybierz opcję `m`, i naciśnij dowolny przycisk, aby rozpocząć kalibrację, która odbywa się poprzez poruszanie sensorem (a zatem i komputerem *Raspberry Pi*). Spróbuj obracać urządzenie w taki sposób, aby znalazło się w każdej możliwej pozycji (pod względem obrotów). Kalibracja kończy się również poprzez naciśnięcie dowolnego przycisku.

        Wybierz opcję `x` aby wyjść z programu kalibracyjnego.

        Domyślnie plik konfiguracyjny jest zapisywany w lokalnym folderze użytkownika, jednak aby używać prawidłowej kalibracji we wszystkich programach, przeniesiemy go w miejsce konfiguracji systemowej:
        `sudo mv ~/.config/sense_hat/RTIMULib.ini /etc`

        /// admonition
        Czujniki IMU potrzebują chwili, aby uruchomić się i skalibrować po uruchomieniu systemu. Po następnym kroku uruchamiającym system ponownie, upewnij się, że urządzenie przez 6-10 sekund po uruchomieniu (~30 sekund łącznie) nie poruszy się, aby uzyskać najdokładniejsze rezultaty.
        ///

        Po tym należy zrestartować programy używające kalibracji, w tym również środowisko tego laboratorium, więc zapisz wykonane zmiany w tym pliku, a następnie użyj komendy do uruchomienia systemu ponownie:
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
def _(sense):
    def set_imu():
        sense.set_imu_config(True, True, False)
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
def _(sense):
    def get_yaw():
        return sense.get_orientation_radians()['yaw']
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
def _(calculate_leds, sense):
    def draw_compass(yaw):
        sense.set_pixels(calculate_leds(yaw))
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
