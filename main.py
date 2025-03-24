import numpy as np
import matplotlib.pyplot as plt


class TransferFunctionSimulator:
    def __init__(self, a1, a0, b2, b1, b0, dt=0.01, T=10):
        self.a1, self.a0 = a1, a0
        self.b2, self.b1, self.b0 = b2, b1, b0
        self.dt = dt
        self.T = T
        self.time = np.arange(0, T, dt)
        self.y = np.zeros_like(self.time)
        self.u = np.zeros_like(self.time)

    def simulate(self, u):
        self.u = u
        x1, x2 = 0, 0  # Stany układu
        for i in range(1, len(self.time)):
            x1_dot = x2
            x2_dot = (-self.b1 * x2 - self.b0 * x1 + self.a1 * u[i] + self.a0 * u[i]) / self.b2
            x1 += x1_dot * self.dt
            x2 += x2_dot * self.dt
            self.y[i] = x1
        return self.time, self.y


class PDController:
    def __init__(self, Kp, Kd):
        self.Kp, self.Kd = Kp, Kd
        self.prev_error = 0

    def control(self, ref, y, dt):
        error = ref - y
        de = (error - self.prev_error) / dt
        self.prev_error = error
        return self.Kp * error + self.Kd * de


def generate_signal(signal_type, time, amplitude=1, frequency=1, duration=1):
    if signal_type == "rectangular":
        return amplitude * ((time % (2 * duration)) < duration)
    elif signal_type == "triangular":
        return amplitude * (2 * np.abs((time / duration) % 2 - 1) - 1)
    elif signal_type == "harmonic":
        return amplitude * np.sin(2 * np.pi * frequency * time)
    else:
        raise ValueError("Unknown signal type")


if __name__ == "__main__":
    # Parametry układu
    a1, a0 = 1, 0
    b2, b1, b0 = 1, 2, 1

    # Parametry regulatora PD
    Kp, Kd = 10, 2

    # Parametry symulacji
    dt, T = 0.01, 10

    simulator = TransferFunctionSimulator(a1, a0, b2, b1, b0, dt, T)
    controller = PDController(Kp, Kd)

    signal_type = "triangular"  # Można zmienić na "rectangular" lub "triangular"
    reference = generate_signal(signal_type, simulator.time)

    y_output = np.zeros_like(simulator.time)
    u_control = np.zeros_like(simulator.time)

    for i in range(1, len(simulator.time)):
        u_control[i] = controller.control(reference[i], y_output[i - 1], dt)
        _, y_output = simulator.simulate(u_control)

    plt.figure()
    plt.plot(simulator.time, reference, label="Reference")
    plt.plot(simulator.time, y_output, label="System Output")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Response")
    plt.title("System Response with PD Control")
    plt.grid()
    plt.show()
