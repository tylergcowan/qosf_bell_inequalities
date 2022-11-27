#import qiskit tools
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile, Aer, IBMQ
from qiskit.tools.monitor import job_monitor, backend_monitor, backend_overview
from pytket.extensions.qiskit import IBMQBackend
#import python stuff
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib
from pytket import Circuit, OpType
from pytket.passes import RemoveRedundancies
from pytket.extensions.qiskit import tk_to_qiskit, qiskit_to_tk
from pytket.utils import expectation_from_counts

def mermin3():
    qc = QuantumCircuit(3,3)

    # this was the first way that cameron said was too complicated!
    """
    qc.h(0)
    qc.h(1)
    qc.cnot(1,2)
    qc.h(1)
    qc.cnot(0,2)
    qc.h(0)
    qc.h(2)
    qc.s(2)
    qc.barrier()
"""
    qc.h(0)
    qc.cnot(0,1)
    qc.cnot(0,2)
    qc.s(0)
    qc.barrier()


    return qc

# generates mermin circuit with 4 qubits
def mermin4():
    qc = QuantumCircuit(4)
    qc.h(0)
    qc.h(2)
    qc.h(3)
    qc.cnot(0,1)
    qc.cnot(2,1)
    qc.h(0)
    qc.rz(np.pi/2,0)
    qc.h(2)
    qc.cnot(3,1)
    qc.h(1)
    qc.h(3)
    qc.barrier()
    #qc.measure_all()
    return qc

def mermin5():
    qc = QuantumCircuit(5)
    qc.h(0)
    qc.h(1)
    qc.h(3)
    qc.h(4)
    qc.cnot(1,2)
    qc.cnot(3,2)
    qc.h(1)
    qc.h(3)
    qc.cnot(4,2)
    qc.cnot(0,2)
    qc.h(0)
    qc.h(2)
    qc.h(4)
    qc.rz(np.pi/2,0)
    qc.barrier()
    #qc.measure_all()
    return qc

print("3 Qubit setup, no measurements applied: ")
print(mermin3())


# converted the qiskit circuit to pytket circuit, so we can optimize + run now

state=qiskit_to_tk(mermin3()).copy()

xxy=Circuit(3,3)
xxy.H(0).H(1).Sdg(2).H(2).add_barrier([0,1,2]).measure_all()

xyx=Circuit(3,3)
xyx.H(0).Sdg(1).H(1).H(2).add_barrier([0,1,2]).measure_all()

yxx=Circuit(3,3)
yxx.Sdg(0).H(0).H(1).H(2).add_barrier([0,1,2]).measure_all()

yyy=Circuit(3,3)
yyy.Sdg(0).H(0).Sdg(1).H(1).Sdg(2).H(2).add_barrier([0,1,2]).measure_all()


circ_list=[]
for m in [xxy, xyx, yxx, yyy]:
    c = state.copy()
    c.append(m)
    circ_list.append(c)

# see mermin inequality in paper for coefficient explanations
#circ_list=[xxy, yyy]
coeff_list= [1.0, 1.0, 1.0, -1.0]

print(tk_to_qiskit(circ_list[0]))
print(tk_to_qiskit(circ_list[1]))
print(tk_to_qiskit(circ_list[2]))
print(tk_to_qiskit(circ_list[3]))



backend = IBMQBackend("ibmq_quito")
circ_list = backend.get_compiled_circuits(circ_list, optimisation_level=2)

handle_list = backend.process_circuits(circ_list, n_shots=12000)
result_list = backend.get_results(handle_list)

expectation = 0
for coeff, result in zip(coeff_list, result_list):
    counts = result.get_counts()
    print()
    print(counts)
    print(coeff)
    expectation += coeff * expectation_from_counts(counts)
    print(expectation_from_counts(counts))
    print(expectation)
    print()


print("final expectation: ", expectation)


#print("Total gate count before compilation =", circ.n_gates)
#print()
# 2 is the highest level. shouldn't be too long with a circuit of this depth
#for ol in range(3):
#    test_circ = circ.copy()
#backend.default_compilation_pass(optimisation_level=2).apply(circ)

# need to make sure the circuit is valid for this specific backend. Fails if not.
#assert backend.valid_circuit(circ)
#    print("Optimisation level", ol)
#    print("Gates", test_circ.n_gates)
#    print("CXs", test_circ.n_gates_of_type(OpType.CX))
#    print()
