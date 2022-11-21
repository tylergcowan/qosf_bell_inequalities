#import qiskit tools
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, Aer, IBMQ
from qiskit.tools.monitor import job_monitor, backend_monitor, backend_overview

#import python stuff
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib
matplotlib.use('TkAgg') # needed this to get plots to display

# Set devices, if using a real device

# These are Tyler's IBMQ credentials
#IBMQ.save_account("c8ae97bdd4de2f3db6b76a1bffc979b4bde93e14e9a19993435b8db857e32d0e38c1f1e9c1d083a9a446a84e26b9bd98ec01eea4191a102457345ab43a48663f")
IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
quito = provider.get_backend('ibmq_quito')

sim = Aer.get_backend('aer_simulator')


def make_chsh_circuit(theta_vec):
    """Return a list of QuantumCircuits for use in a CHSH experiemnt
    (one for each value of theta in theta_vec)

        Args:
            theta_vec (list): list of values of angles between the bases of Alice and Bob

        Returns:
            List[QuantumCircuit]: CHSH QuantumCircuits for each value of theta
    """
    chsh_circuits = []

    for theta in theta_vec:
        obs_vec = ['00', '01', '10', '11']
        for el in obs_vec:
            qc = QuantumCircuit(2, 2)
            qc.h(0)
            qc.cx(0, 1)
            qc.ry(theta, 0)
            for a in range(2):
                if el[a] == '1':
                    qc.h(a)
            qc.measure(range(2), range(2))
            chsh_circuits.append(qc)

    return chsh_circuits


def compute_chsh_witness(counts):
    """Computes expectation values for the CHSH inequality, for each
    angle (theta) between measurement axis.

        Args: counts (list[dict]): dict of counts for each experiment
              (4 per value of theta)

        Returns:
            Tuple(List, List): Tuple of lists with the two CHSH witnesses
    """
    # Order is ZZ,ZX,XZ,XX

    CHSH1 = []
    CHSH2 = []
    # Divide the list of dictionaries in sets of 4
    for i in range(0, len(counts), 4):
        theta_dict = counts[i:i + 4]
        zz = theta_dict[0]
        zx = theta_dict[1]
        xz = theta_dict[2]
        xx = theta_dict[3]

        no_shots = sum(xx[y] for y in xx)

        chsh1 = 0
        chsh2 = 0

        for element in zz:
            parity = (-1) ** (int(element[0]) + int(element[1]))
            chsh1 += parity * zz[element]
            chsh2 += parity * zz[element]

        for element in zx:
            parity = (-1) ** (int(element[0]) + int(element[1]))
            chsh1 += parity * zx[element]
            chsh2 -= parity * zx[element]

        for element in xz:
            parity = (-1) ** (int(element[0]) + int(element[1]))
            chsh1 -= parity * xz[element]
            chsh2 += parity * xz[element]

        for element in xx:
            parity = (-1) ** (int(element[0]) + int(element[1]))
            chsh1 += parity * xx[element]
            chsh2 += parity * xx[element]

        CHSH1.append(chsh1 / no_shots)
        CHSH2.append(chsh2 / no_shots)

    return CHSH1, CHSH2


number_of_thetas = 15
theta_vec = np.linspace(0,2*np.pi,number_of_thetas)
my_chsh_circuits = make_chsh_circuit(theta_vec)

print(my_chsh_circuits[4].draw())
print(my_chsh_circuits[5].draw())
print(my_chsh_circuits[6].draw())
print(my_chsh_circuits[7].draw())


# Execute and get counts
result_ideal = sim.run(my_chsh_circuits).result()

tic = time.time()
transpiled_circuits = transpile(my_chsh_circuits, quito)
job_real = quito.run(transpiled_circuits, shots=8192)
job_monitor(job_real)
result_real = job_real.result()
toc = time.time()

print(toc-tic)

CHSH1_ideal, CHSH2_ideal = compute_chsh_witness(result_ideal.get_counts())
CHSH1_real, CHSH2_real = compute_chsh_witness(result_real.get_counts())

plt.figure(figsize=(12,8))
plt.rcParams.update({'font.size': 22})
plt.plot(theta_vec,CHSH1_ideal,'o-',label = 'CHSH1 Noiseless')
plt.plot(theta_vec,CHSH2_ideal,'o-',label = 'CHSH2 Noiseless')

plt.plot(theta_vec,CHSH1_real,'x-',label = 'CHSH1 Quito')
plt.plot(theta_vec,CHSH2_real,'x-',label = 'CHSH2 Quito')

plt.grid(which='major',axis='both')
plt.rcParams.update({'font.size': 16})
plt.legend()
plt.axhline(y=2, color='r', linestyle='-')
plt.axhline(y=-2, color='r', linestyle='-')
plt.axhline(y=np.sqrt(2)*2, color='k', linestyle='-.')
plt.axhline(y=-np.sqrt(2)*2, color='k', linestyle='-.')
plt.xlabel('Theta')
plt.ylabel('CHSH witness')

plt.show()
