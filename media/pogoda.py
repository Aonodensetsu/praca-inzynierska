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
def _(bme280, ltr559):
    def update_sensors():
        bme280.update_sensor()
        ltr559.update_sensor()
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
def _(
    Metric,
    bme280,
    compensate_temperature,
    get_cpu_temperature,
    ltr559,
    proximity_to_mm,
    sph0645lm4h_b,
):
    metrics = [
        Metric('CPU',   '°C',  lambda: get_cpu_temperature()),
        # dodaj linijki metryk dla temperatury, ciśnienia, wilgotności, bliskości, jasności, głośności SPL
        Metric('T',     '°C',  lambda: compensate_temperature(bme280.temperature)),
        Metric('p',     'hPa', lambda: bme280.pressure),
        Metric('RH',    '%',   lambda: bme280.humidity),
        Metric('prox',  'mm',  lambda: proximity_to_mm(ltr559.get_proximity(passive=True))),
        Metric('light', 'Lux', lambda: ltr559.get_lux(passive=True)),
        Metric('noise', 'dB',  lambda: sph0645lm4h_b.spl()),
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
def _(ntfy_topic, post, values):
    def send_message():
        if values['prox'][-1] < 1:
            post(f'https://ntfy.sh/{ntfy_topic}', json={k: v[-1] for k, v in values.items()})
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
def _(
    data_loop,
    display_text,
    insert_vals,
    metrics,
    send_message,
    sleep,
    update_sensors,
):
    async def loop():
        update_sensors()
        for metric in data_loop(metrics):
            update_sensors()
            insert_vals(metrics)
            send_message()
            display_text(metric)
            await sleep(1)
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
    sph0645lm4h_b = SPH0645LM4H_B(spl_base=40, dbms_base=-76)
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
