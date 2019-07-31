import numpy as np
import matplotlib.pyplot as plt

SAMPLING_FREQUENCY = 200


def load_data(acq_path):

    data = np.loadtxt(acq_path, dtype=str)

    data0 = np.array([d.split(',') for d in data[:, 1] if d.split(',')[1][:2] == '/0'])
    data1 = np.array([d.split(',') for d in data[:, 1] if d.split(',')[1][:2] == '/1'])

    data0 = data0[:, 2:].astype(float)
    data1 = data1[:, 2:].astype(float)

    t0 = np.arange(len(data0)) / SAMPLING_FREQUENCY
    t1 = np.arange(len(data1)) / SAMPLING_FREQUENCY

    return t1, t0, data0, data1


if __name__ == '__main__':


    fs = 200

    t1, t0, data0, data1 = load_data('../acquisitions/catch.csv')

    onset = (np.convolve(data0[:, 0] < -6, np.ones(50), 'full')[:len(t0)] > 0.5).astype(int)

    np.savetxt('catch_data.csv', np.hstack((t0.reshape(-1, 1), data0[:, :3], onset.reshape(-1, 1))), delimiter=',')


