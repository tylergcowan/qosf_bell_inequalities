from qiskit import QuantumCircuit
from pytket.extensions.qiskit import IBMQBackend
from pytket import Circuit
from pytket.extensions.qiskit import tk_to_qiskit, qiskit_to_tk
from pytket.utils import expectation_from_counts

def mermin3():
    """
    :return: qc, GHZ state circuit with 3 qubits
    """
    qc = QuantumCircuit(3,3)

    # Foreman paper GHZ state. This yielded results as high as 3.27.
    #qc.h(0)
    #qc.cnot(0,1)
    #qc.cnot(0,2)
    #qc.s(0)
    #qc.barrier()

    # typical GHZ(+) state
    qc.h(0)
    qc.cnot(0,1)
    qc.cnot(1,2)
    qc.barrier()


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

    return qc

# converted the qiskit circuit to pytket circuit, so we can optimize + run now
state=qiskit_to_tk(mermin3()).copy()

# the M4 and M5 will require several (10+) different measurement types. So, instead generalize this process
#m3=["yxx", "xyx", "xxy", "yyy"]

#this m3 is for the typical gh state. the above is for foreman GHZ
m3=["yyx", "yxy", "xyy", "xxx"]
m4=["yxxx", "xyxx", "xxyx", "xxxy", "yyxx", "yxyx", "yxxy", "xyyx", "xyxy", "xxyy", "yyyy", "xxxx", "yyyx", "yyxy", "xyyy", "xyyy"]
m5=["yxxxx", "xyxxx", "xxyxx", "xxxyx", "xxxxy",    "yyyxx", "yyxyx", "yyxxy", "yxyyx", "yxyxy", "yxxyy", "xyyyx", "xyyxy", "xyxyy", "xxyyy", "yyyy"]

# see mermin inequality in paper for coefficient explanations
#coeff_3= [1.0, 1.0, 1.0, -1.0]

# this is for typical GHZ. above is for cameron GHZ
coeff_3= [-1.0, -1.0, -1.0, 1.0]
coeff_4= [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1]
coeff_5= [1,1,1,1,1, -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

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
    qc.measure_all()

    return qc

circ_list=[]

# append measurements in x/y bases
for m in m3:
    c = state.copy()
    c.append(measurements(m))
    circ_list.append(c)

#exit(1)

backend = IBMQBackend("ibmq_lima")
circ_list = backend.get_compiled_circuits(circ_list, optimisation_level=2)

handle_list = backend.process_circuits(circ_list, n_shots=20000)
result_list = backend.get_results(handle_list)

expectation = 0
for coeff, result in zip(coeff_3, result_list):
    counts = result.get_counts()
    expectation += coeff * expectation_from_counts(counts)

# computed value of the mermin polynomial
print("final expectation: ", expectation)