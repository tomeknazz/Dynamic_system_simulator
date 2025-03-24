import numpy as np  # Import biblioteki NumPy do operacji numerycznych
import matplotlib.pyplot as plt  # Import biblioteki do wizualizacji wyników


class TransferFunctionSimulator:
    def __init__(self, a1, a0, b2, b1, b0, dt=0.01, T=10):
        # Inicjalizacja parametrów układu
        self.a1, self.a0 = a1, a0
        self.b2, self.b1, self.b0 = b2, b1, b0
        self.dt = dt  # Krok czasowy symulacji
        self.T = T  # Całkowity czas symulacji
        self.time = np.arange(0, T, dt)  # Wektor czasu
        self.y = np.zeros_like(self.time)  # Inicjalizacja odpowiedzi układu
        self.u = np.zeros_like(self.time)  # Inicjalizacja sygnału wejściowego

    def simulate(self, u):
        # Symulacja układu dla zadanego sygnału wejściowego
        self.u = u
        x1, x2 = 0, 0  # Stany układu (x1 = wyjście, x2 = pochodna x1)
        for i in range(1, len(self.time)):
            x1_dot = x2  # Pochodna pierwszego stanu
            x2_dot = (-self.b1 * x2 - self.b0 * x1 + self.a1 * u[i] + self.a0 * u[
                i]) / self.b2  # Pochodna drugiego stanu
            x1 += x1_dot * self.dt  # Aktualizacja pierwszego stanu
            x2 += x2_dot * self.dt  # Aktualizacja drugiego stanu
            self.y[i] = x1  # Zapisanie wartości wyjścia
        return self.time, self.y


class PDController:
    def __init__(self, Kp, Kd):
        # Inicjalizacja parametrów regulatora PD
        self.Kp, self.Kd = Kp, Kd
        self.prev_error = 0  # Poprzedni błąd dla wyliczenia pochodnej

    def control(self, ref, y, dt):
        # Obliczanie wartości sterowania na podstawie regulatora PD
        error = ref - y  # Obliczenie błędu
        de = (error - self.prev_error) / dt  # Przybliżona pochodna błędu
        self.prev_error = error  # Aktualizacja błędu
        return self.Kp * error + self.Kd * de  # Wyliczenie sygnału sterującego


def generate_signal(signal_type, time, amplitude=1, frequency=1, duration=1):
    # Generowanie różnych typów sygnałów wejściowych
    if signal_type == "rectangular":
        return amplitude * ((time % (2 * duration)) < duration)  # Sygnał prostokątny
    elif signal_type == "triangular":
        return amplitude * (2 * np.abs((time / duration) % 2 - 1) - 1)  # Sygnał trójkątny
    elif signal_type == "harmonic":
        return amplitude * np.sin(2 * np.pi * frequency * time)  # Sygnał harmoniczny
    else:
        raise ValueError("Unknown signal type")  # Obsługa błędnego typu sygnału


if __name__ == "__main__":
    # Parametry układu
    a1, a0 = 1, 0  # Parametry licznika transmitancji
    b2, b1, b0 = 1, 2, 1  # Parametry mianownika transmitancji

    # Parametry regulatora PD
    Kp, Kd = 10, 2  # Wzmocnienia regulatora PD

    # Parametry symulacji
    dt, T = 0.01, 10  # Krok czasowy i całkowity czas symulacji

    simulator = TransferFunctionSimulator(a1, a0, b2, b1, b0, dt, T)  # Inicjalizacja symulatora układu
    controller = PDController(Kp, Kd)  # Inicjalizacja regulatora PD

    signal_type = "harmonic"  # Można zmienić na "rectangular" lub "triangular"
    reference = generate_signal(signal_type, simulator.time)  # Generowanie sygnału referencyjnego

    y_output = np.zeros_like(simulator.time)  # Inicjalizacja wektora odpowiedzi układu
    u_control = np.zeros_like(simulator.time)  # Inicjalizacja sygnału sterującego

    for i in range(1, len(simulator.time)):
        u_control[i] = controller.control(reference[i], y_output[i - 1], dt)  # Obliczenie wartości sterowania
        _, y_output = simulator.simulate(u_control)  # Symulacja układu dla sygnału sterującego

    plt.figure()
    plt.plot(simulator.time, reference, label="Reference")  # Wykres sygnału referencyjnego
    plt.plot(simulator.time, y_output, label="System Output")  # Wykres odpowiedzi układu
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Response")
    plt.title("System Response with PD Control")
    plt.grid()
    plt.show()  # Wyświetlenie wykresu