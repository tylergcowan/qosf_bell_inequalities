from qiskit import QuantumCircuit
from pytket.extensions.qiskit import IBMQBackend
from pytket import Circuit
from pytket.extensions.qiskit import qiskit_to_tk, tk_to_qiskit
from pytket.utils import expectation_from_counts

def mermin3():
    """
    :return: qc, GHZ state circuit with 3 qubits
    """
    qc = QuantumCircuit(3,3)

    # Foreman paper GHZ state. This yielded results as high as 3.27.
    qc.h(0)
    qc.cnot(0,1)
    qc.cnot(0,2)
    qc.s(0)
    qc.barrier()

    # typical GHZ(+) state
    #qc.h(0)
    #qc.cnot(0,1)
    #qc.cnot(1,2)
    #qc.barrier()

    return qc

def mermin4():
    """
    :return: qc, GHZ state circuit with 4 qubits
    """
    qc = QuantumCircuit(4)

    # GHZ Foreman state
    qc.h(0)
    qc.cnot(0, 1)
    qc.cnot(0, 2)
    qc.cnot(0, 3)
    qc.s(0)
    qc.barrier()

    # typical GHZ(+) state
    #qc.h(0)
    #qc.cnot(0,1)
    #qc.cnot(1,2)
    #qc.cnot(2,3)
    #qc.barrier()

    return qc

def mermin5():
    """
    :return: qc, GHZ state circuit with 5 qubits
    """

    qc = QuantumCircuit(5)

    # GHZ Foreman state
    qc.h(0)
    qc.cnot(0, 1)
    qc.cnot(0, 2)
    qc.cnot(0, 3)
    qc.cnot(0, 4)
    qc.s(0)
    qc.barrier()

    # ghz pure
    #qc.h(0)
    #qc.cnot(0,1)
    #qc.cnot(1,2)
    #qc.cnot(2,3)
    #qc.cnot(3,4)
    #qc.barrier()

    return qc

# converted the qiskit circuit to pytket circuit, so we can optimize + run now
state=qiskit_to_tk(mermin5()).copy()

# These are the measurements to be performed on the 3/4/5-qubit mermin inequalities

m3=["xxy", "xyx", "yxx", "yyy"]
coeff_3= [1.0, 1.0, 1.0, -1.0]

m4=["xxxy", "xxyx", "xyxx", "yxxx", "xyyy", "yxyy", "yyxy", "yyyx"]
coeff_4=[1, 1, 1, 1, -1, -1, -1, -1]

m5=["xxxxy", "xxxyx", "xxyxx", "xyxxx", "yxxxx",   "xxyyy", "xyyxy", "xyyyx", "xyxyy", "yyyxx", "yyxyx", "yyxxy", "yxyyx", "yxyxy", "yxxyy", "yyyyy"]
coeff_5=[1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1]


def measurements(string):
    """
    :param string: Sequence of bases for measurements (e.g. XXY, YXYY, XXYYX)
    :return: qc: quantum circuit to project measurements into Y or X bases
    """
    qc = Circuit(len(string),len(string))

    for i in range (0,len(string)):

        # x measurement basis
        if string[i] == "x":
            qc.H(i)

        # y measurement basis
        else:
            qc.Sdg(i)
            qc.H(i)

    # barrier used to isolate sections which Pytket can optimize
    qc.add_barrier(range(0,len(string)))
    #qc.Measure(0,1)
    #qc.Measure(1,0)
    #qc.Measure(2,2)
    qc.measure_all()

    return qc

circ_list=[]

# append measurements in x/y bases
for m in m5:
    c = state.copy()
    c.append(measurements(m))
    circ_list.append(c)
    print(tk_to_qiskit(c))

backend = IBMQBackend("ibmq_quito")
circ_list = backend.get_compiled_circuits(circ_list, optimisation_level=0)

handle_list = backend.process_circuits(circ_list, n_shots=16384)
result_list = backend.get_results(handle_list)

expectation = 0
for coeff, result in zip(coeff_5, result_list):
    counts = result.get_counts()
    expectation += coeff * expectation_from_counts(counts)
    print(expectation_from_counts(counts), coeff)

# computed value of the mermin polynomial
print("final expectation: ", expectation)