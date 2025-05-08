import matplotlib.pyplot as plt  # Import biblioteki do wizualizacji wyników
import numpy as np  # Import biblioteki NumPy do operacji numerycznych


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


def menu():
    menu_text = """
========= Wybierz typ sygnału wejściowego =========
\t[1] Prostokątny
\t[2] Trójkątny
\t[3] Harmoniczny
\t[q] Wyjście
===================================================
"""
    # Wyświetlenie menu wyboru sygnału

    while True:
        choice = input(menu_text)
        if choice == '1':
            return "rectangular"
        elif choice == '2':
            return "triangular"
        elif choice == '3':
            return "harmonic"
        elif choice == 'q':
            exit(0)
        else:
            print("Niepoprawny wybór, spróbuj ponownie.")
            # przerób to na switch case


if __name__ == "__main__":
    user_choice = ""
    while True:
        if user_choice == 0:
            print("Czy chcesz ponownie wykonać symulację? \n[1] Tak \n[2] Nie")
            if (input() == "1"):
                user_choice = 1
                print("Czy chcesz zmenić parametry układu?")
                print("Wzór układu G(s) = (a1*s + a0) / (b2*s^2 + b1*s + b0)")
                while True:
                    print(f"[1] a1 = {a1}\n[2] a0 = {a0}\n[3] b2 = {b2}\n[4] b1 = {b1}\n[5] b0 = {b0}\n[6] Kp = {Kp}\n[7] Kd = {Kd}\n[8] Zmień rodzaj sygnału\n[9] Nie chce zmieniać parametrów")
                    match int(input()):
                        case 1:
                            a1 = float(input("Podaj parametr a1: "))
                            continue
                        case 2:
                            a0 = float(input("Podaj parametr a0: "))
                            continue
                        case 3:
                            b2 = float(input("Podaj parametr b2: "))
                            continue
                        case 4:
                            b1 = float(input("Podaj parametr b1: "))
                            continue
                        case 5:
                            b0 = float(input("Podaj parametr b0: "))
                            continue
                        case 6:
                            Kp = float(input("Podaj parametr Kp: "))
                            continue
                        case 7:
                            Kd = float(input("Podaj parametr Kd: "))
                            continue
                        case 8:
                            signal_type = menu()
                            print("Wybrany typ sygnału:", signal_type)
                            continue
                        case 9:
                            break
                        case default:
                            print("Niepoprawny wybór, spróbuj ponownie.")
                            signal_type = 0
                            continue
            else:
                exit(0)
        if user_choice != 1:
            signal_type = menu()
            print("Wybrany typ sygnału:", signal_type)  # Wyświetlenie wybranego typu sygnału
            print("Wzór układu G(s) = (a1*s + a0) / (b2*s^2 + b1*s + b0)")  # Wzór układu
            # Parametry układu
            a1 = float(input("Podaj parametr a1: "))
            a0 = float(input("Podaj parametr a0: "))
            b2 = float(input("Podaj parametr b2: "))
            b1 = float(input("Podaj parametr b1: "))
            b0 = float(input("Podaj parametr b0: "))
            # Parametry regulatora PD
            Kp = float(input("Podaj parametr Kp: "))
            Kd = float(input("Podaj parametr Kd: "))

        # Parametry symulacji
        dt, T = 0.01, 10  # Krok czasowy i całkowity czas symulacji

        simulator = TransferFunctionSimulator(a1, a0, b2, b1, b0, dt, T)  # Inicjalizacja symulatora układu
        controller = PDController(Kp, Kd)  # Inicjalizacja regulatora PD

        # Można zmienić na "rectangular" lub "triangular"
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
        user_choice = 0
