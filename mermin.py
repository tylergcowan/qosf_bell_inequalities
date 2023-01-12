from qiskit import QuantumCircuit
from pytket.extensions.qiskit import IBMQBackend
from pytket import Circuit
from pytket.extensions.qiskit import qiskit_to_tk, tk_to_qiskit
from pytket.utils import expectation_from_counts
import numpy as np

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

def svet3():
    """
    :return: qc, GHZ state circuit with 3 qubits
    """
    qc = QuantumCircuit(3,3)

    # typical GHZ(+) state
    qc.h(0)
    qc.cnot(0,1)
    qc.cnot(1,2)
    qc.barrier()

    return qc

def svet4():
    """
    :return: qc, GHZ state circuit with 4 qubits
    """
    qc = QuantumCircuit(4,4)

    # typical GHZ(+) state
    qc.h(0)
    qc.cnot(0,1)
    qc.cnot(1,2)
    qc.cnot(2,3)
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

def mermin6():
    """
    :return: qc, GHZ state circuit with 6 qubits
    """
    qc = QuantumCircuit(6)

    # GHZ Foreman state
    qc.h(0)
    qc.cnot(0, 1)
    qc.cnot(0, 2)
    qc.cnot(0, 3)
    qc.cnot(0, 4)
    qc.cnot(0, 5)
    qc.s(0)
    qc.barrier()

    return qc

def mermin7():
    """
    :return: qc, GHZ state circuit with 7 qubits
    """
    qc = QuantumCircuit(7)

    # GHZ Foreman state
    qc.h(0)
    qc.cnot(0, 1)
    qc.cnot(0, 2)
    qc.cnot(0, 3)
    qc.cnot(0, 4)
    qc.cnot(0, 5)
    qc.cnot(0, 6)
    qc.s(0)
    qc.barrier()

    return qc


# converted the qiskit circuit to pytket circuit, so we can optimize + run now
state=qiskit_to_tk(svet4()).copy()

# Mermin measurements for iGHZ state.
m3=["xxy", "xyx", "yxx", "yyy"]
coeff_m3= [1.0, 1.0, 1.0, -1.0]
m4=["xxxy", "xxyx", "xyxx", "yxxx", "xyyy", "yxyy", "yyxy", "yyyx"]
coeff_m4=[1, 1, 1, 1, -1, -1, -1, -1]
m5=["xxxxy", "xxxyx", "xxyxx", "xyxxx", "yxxxx",   "xxyyy", "xyyxy", "xyyyx", "xyxyy", "yyyxx", "yyxyx", "yyxxy", "yxyyx", "yxyxy", "yxxyy", "yyyyy"]
coeff_m5=[1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1]
m6=["xxxxxy", "xxxxyx", "xxxyxx", "xxyxxx", "xyxxxx", "yxxxxx",

    "xxxyyy","xxyxyy",
    "xxyyxy","xxyyyx",
    "xyxxyy","xyxyxy",
    "xyxyyx","xyyxxy",
    "xyyxyx","xyyyxx",
    "yxxxyy","yxxyxy",
    "yxxyyx","yxyxxy",
    "yxyxyx","yxyyxx",
    "yyxxxy","yyxxyx",
    "yyxyxx","yyyxxx",

    "yyyyyx", "yyyyxy", "yyyxyy", "yyxyyy", "yxyyyy", "xyyyyy"]
coeff_m6=[1, 1, 1, 1, 1, 1,
          -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
         1, 1, 1, 1, 1, 1]
m7=["xxxxxxy", "xxxxxyx", "xxxxyxx", "xxxyxxx", "xxyxxxx", "xyxxxxx", "yxxxxxx",

    # 35 with 3 y's
    "xxxxyyy", "xxxyxyy",
    "xxxyyxy", "xxxyyyx",
    "xxyxxyy", "xxyxyxy",
    "xxyxyyx", "xxyyxxy",
    "xxyyxyx", "xxyyyxx",
    "xyxxxyy", "xyxxyxy",
    "xyxxyyx", "xyxyxxy",
    "xyxyxyx", "xyxyyxx",
    "xyyxxxy", "xyyxxyx",
    "xyyxyxx", "xyyyxxx",
    "yxxxxyy", "yxxxyxy",
    "yxxxyyx", "yxxyxxy",
    "yxxyxyx", "yxxyyxx",
    "yxyxxxy", "yxyxxyx",
    "yxyxyxx", "yxyyxxx",
    "yyxxxxy", "yyxxxyx",
    "yyxxyxx", "yyxyxxx",
    "yyyxxxx",

    # 21 with 5 y's
    "xxyyyyy", "xyxyyyy",
    "xyyxyyy", "xyyyxyy",
    "xyyyyxy", "xyyyyyx",
    "yxxyyyy", "yxyxyyy",
    "yxyyxyy", "yxyyyxy",
    "yxyyyyx", "yyxxyyy",
    "yyxyxyy", "yyxyyxy",
    "yyxyyyx", "yyyxxyy",
    "yyyxyxy", "yyyxyyx",
    "yyyyxxy", "yyyyxyx",
    "yyyyyxx",

    "yyyyyyy"
    ]
coeff_m7=[1, 1, 1, 1, 1, 1, 1,

          -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
          -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,

          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,

          -1
          ]

# Svetlichny measurements
s3=["xxc", "xxd", "xyc", "yxc", "yyd", "yyc", "yxd", "xyd"]
coeff_s3=[1, 1, 1, 1, -1, -1, -1, -1]

# let's try swapping x and  y.
#s4=["xxxx", "yxxx", "xyxx", "xxyx", "xxxy", "yyxx", "yxyx", "yxxy",
#    "xyyx", "xyxy", "xxyy", "yyyx", "yyxy", "yxyy", "xyyy", "yyyy"
#    ]
s4=["yyyy", "xyyy", "yxyy", "yyxy", "yyyx", "xxyy", "xyxy", "xyyx",
    "yxxy", "yxyx", "yyxx", "xxxy", "xxyx", "xyxx", "yxxx", "xxxx"
    ]
coeff_s4=[1, -1, -1, -1,
          -1, -1, -1, -1,
          -1, -1, -1, 1,
          1, 1, 1, 1]

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
        elif string[i] == "y":
            qc.Sdg(i)
            qc.H(i)

        # c=y-x/sqrt(2)
        elif string[i] == "c":
            qc.Tdg(i)
            qc.Sdg(i)
            qc.H(i)

        # equivalent of c'= -(X+Y)/sqrt(2)
        elif string[i] == "d":
            qc.T(i)
            qc.S(i)
            qc.H(i)

        else:
            print("ERROR! unrecognized symbol: ",string[i])
            exit(1)

    # barrier used to isolate sections which Pytket can optimize
    qc.add_barrier(range(0,len(string)))
    qc.measure_all()

    return qc

circ_list=[]

# append measurements in x/y bases
for m in s4:
    c = state.copy()
    c.append(measurements(m))
    circ_list.append(c)
    print(tk_to_qiskit(c))


backend = IBMQBackend("ibmq_belem")
circ_list = backend.get_compiled_circuits(circ_list, optimisation_level=2)

handle_list = backend.process_circuits(circ_list, n_shots=16384)
result_list = backend.get_results(handle_list)

expectation = 0
for coeff, result in zip(coeff_s4, result_list):
    counts = result.get_counts()
    expectation += coeff * expectation_from_counts(counts)
    print(expectation_from_counts(counts), coeff)

# computed value of the mermin polynomial
print("final expectation: ", expectation)