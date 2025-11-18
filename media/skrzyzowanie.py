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
def _(GPIO):
    def gpio_config():
        GPIO.setmode(GPIO.BOARD)
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
    led_red = 16
    led_yellow = 18
    led_green = 22
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
def _(GPIO, led_green, led_red, led_yellow):
    def port_config():
        GPIO.setup(led_red, GPIO.OUT)
        GPIO.setup(led_yellow, GPIO.OUT)
        GPIO.setup(led_green, GPIO.OUT)
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
def _(GPIO, led_green, led_red, led_yellow, sleep):
    async def red_to_green():
        GPIO.output(led_yellow, GPIO.HIGH)
        await sleep(2)
        GPIO.output(led_green, GPIO.HIGH)
        GPIO.output(led_red, GPIO.LOW)
        GPIO.output(led_yellow, GPIO.LOW)

    async def green_to_red():
        GPIO.output(led_yellow, GPIO.HIGH)
        GPIO.output(led_green, GPIO.LOW)
        await sleep(2)
        GPIO.output(led_red, GPIO.HIGH)
        GPIO.output(led_yellow, GPIO.LOW)
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
def _(receive_task):
    receive_task(duration=30)
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
def _(asyncio, green_to_red, ntfy_topic, red_to_green):
    import requests
    import json

    async def sender():
        for i in range(3):
            await green_to_red()
            await asyncio.sleep(5)
            requests.post(f"https://ntfy.sh/{ntfy_topic}", data=b'rg')
            await asyncio.sleep(20)
            requests.post(f"https://ntfy.sh/{ntfy_topic}", data=b'gr')
            await asyncio.sleep(5)
            await red_to_green()
            await asyncio.sleep(20)
        requests.post(f"https://ntfy.sh/{ntfy_topic}", data=b'stop')

    async def receiver():
        resp = requests.get(f"https://ntfy.sh/{ntfy_topic}/json", stream=True)
        for line in resp.iter_lines():
            try:
                j = json.loads(line)
                match j['message']:
                    case 'rg':
                        await red_to_green()
                    case 'gr':
                        await green_to_red()
                    case 'stop':
                        break
            except:
                pass
    return json, receiver, requests, sender


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


    ntfy_task_completed = True

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
