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
        self.u = u
        x1, x2 = 0, 0
        for i in range(1, len(self.time)):
            x1_dot = x2
            u_dot = (u[i] - u[i - 1]) / self.dt
            x2_dot = (-self.b1 * x2 - self.b0 * x1 + self.a1 * u_dot + self.a0 * u[i]) / self.b2
            x1 += x1_dot * self.dt
            x2 += x2_dot * self.dt
            self.y[i] = x1
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


if __name__ == "__main__":
    # Domyślne parametry układu
    default_params = {
        "a1": 1.0,
        "a0": 1.0,
        "b2": 1.0,
        "b1": 1.0,
        "b0": 1.0,
        "Kp": 1.0,
        "Kd": 1.0
    }
    
    # Inicjalizacja parametrów z domyślnymi wartościami
    a1 = default_params["a1"]
    a0 = default_params["a0"]
    b2 = default_params["b2"]
    b1 = default_params["b1"]
    b0 = default_params["b0"]
    Kp = default_params["Kp"]
    Kd = default_params["Kd"]
    
    signal_type = "rectangular"  # Domyślny typ sygnału
    run_simulation = True
    
    while run_simulation:
        # Wybór typu sygnału
        print("\nWybierz typ sygnału:")
        signal_type = menu()
        print("Wybrany typ sygnału:", signal_type)
        
        # Wybór parametrów
        print("\nParametry układu G(s) = (a1*s + a0) / (b2*s^2 + b1*s + b0)")
        print("[1] Użyj domyślnych parametrów (wszystkie = 1.0)")
        print("[2] Wprowadź własne parametry")
        
        param_choice = input("Wybór: ")
        
        if param_choice == "2":
            # Wprowadzanie własnych parametrów
            a1 = float(input(f"Podaj parametr a1 [{a1}]: ") or a1)
            a0 = float(input(f"Podaj parametr a0 [{a0}]: ") or a0)
            b2 = float(input(f"Podaj parametr b2 [{b2}]: ") or b2)
            b1 = float(input(f"Podaj parametr b1 [{b1}]: ") or b1)
            b0 = float(input(f"Podaj parametr b0 [{b0}]: ") or b0)
            Kp = float(input(f"Podaj parametr Kp [{Kp}]: ") or Kp)
            Kd = float(input(f"Podaj parametr Kd [{Kd}]: ") or Kd)
        else:
            # Używamy domyślnych parametrów
            print("Używam domyślnych parametrów (wszystkie = 1.0)")
        
        # Flaga kontrolująca czy uruchomić symulację
        run_sim_now = True
        
        while run_sim_now:
            # Wyświetlenie aktualnych parametrów
            print("\nAktualne parametry:")
            print(f"a1 = {a1}, a0 = {a0}")
            print(f"b2 = {b2}, b1 = {b1}, b0 = {b0}")
            print(f"Kp = {Kp}, Kd = {Kd}")
            print(f"Typ sygnału: {signal_type}")
            
            # Parametry symulacji
            dt, T = 0.01, 10  # Krok czasowy i całkowity czas symulacji

            simulator = TransferFunctionSimulator(a1, a0, b2, b1, b0, dt, T)  # Inicjalizacja symulatora układu
            controller = PDController(Kp, Kd)  # Inicjalizacja regulatora PD

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
            
            # Pytanie o ponowne uruchomienie symulacji
            print("\nCzy chcesz ponownie wykonać symulację?")
            print("[1] Tak")
            print("[2] Nie")
            if input() != "1":
                run_simulation = False
                run_sim_now = False
            else:
                # Pytanie o zmianę parametrów
                print("\nCo chcesz zrobić?")
                print("[1] Użyć aktualnych parametrów")
                print("[2] Zmienić parametry")
                print("[3] Wrócić do domyślnych parametrów")
                modify_choice = input()
                
                if modify_choice == "2":
                    print("\nZmienianie parametrów:")
                    param_changing = True
                    while param_changing:
                        print(f"[1] a1 = {a1}\n[2] a0 = {a0}\n[3] b2 = {b2}\n[4] b1 = {b1}\n[5] b0 = {b0}\n[6] Kp = {Kp}\n[7] Kd = {Kd}")
                        print("[8] Zmień rodzaj sygnału\n[9] Gotowe - kontynuuj symulację")
                        
                        try:
                            param_to_change = int(input("Wybierz parametr do zmiany: "))
                            if param_to_change == 9:
                                param_changing = False  # Wyjście z pętli zmiany parametrów
                            elif param_to_change == 8:
                                signal_type = menu()
                                print("Wybrany typ sygnału:", signal_type)
                            elif 1 <= param_to_change <= 7:
                                param_names = ["a1", "a0", "b2", "b1", "b0", "Kp", "Kd"]
                                param_vars = [a1, a0, b2, b1, b0, Kp, Kd]
                                param_name = param_names[param_to_change-1]
                                current_value = param_vars[param_to_change-1]
                                
                                new_value = input(f"Podaj nową wartość dla {param_name} [{current_value}]: ")
                                if new_value:
                                    if param_to_change == 1:
                                        a1 = float(new_value)
                                    elif param_to_change == 2:
                                        a0 = float(new_value)
                                    elif param_to_change == 3:
                                        b2 = float(new_value)
                                    elif param_to_change == 4:
                                        b1 = float(new_value)
                                    elif param_to_change == 5:
                                        b0 = float(new_value)
                                    elif param_to_change == 6:
                                        Kp = float(new_value)
                                    elif param_to_change == 7:
                                        Kd = float(new_value)
                            else:
                                print("Niepoprawny wybór, spróbuj ponownie.")
                        except ValueError:
                            print("Podaj poprawną liczbę.")
                elif modify_choice == "3":
                    # Przywrócenie domyślnych parametrów
                    a1 = default_params["a1"]
                    a0 = default_params["a0"]
                    b2 = default_params["b2"]
                    b1 = default_params["b1"]
                    b0 = default_params["b0"]
                    Kp = default_params["Kp"]
                    Kd = default_params["Kd"]
                    print("Przywrócono domyślne parametry (wszystkie = 1.0)")
                elif modify_choice == "1":
                    # Kontynuuj z aktualnymi parametrami
                    pass
                else:
                    print("Niepoprawny wybór, używam aktualnych parametrów.")
