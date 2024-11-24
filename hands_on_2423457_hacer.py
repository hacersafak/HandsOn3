# -*- coding: utf-8 -*-
"""Hands-On-2423457-Hacer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RtI0VZkCO58fp31OwHAzsmznfCN-h2RN
"""

# how to implement one way a bigger basis set for the H 2  molecule (6-31g instead of STO-3G). This will create a bigger "PauliWord" that contains 8-long sentences.
# Here, we have used Jordan-Wigner mapping to map fermionic operators to qubits. We will talk about the exact details of "qubitization" later.

!pip install qiskit_nature
!pip install --prefer-binary pyscf
!pip install qiskit_ibm_runtime

from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper

driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="6-31g",
    charge=0,
    spin=0,
    unit=DistanceUnit.ANGSTROM,
)

es_problem = driver.run()
fermionic_op = es_problem.hamiltonian.second_q_op()



mapper = JordanWignerMapper()

qubit_jw_op = mapper.map(fermionic_op)
print(qubit_jw_op)

#Now modify the above VQD example to obtain the the ground state, and first two excited states. Do you see a difference?
from qiskit_algorithms.optimizers import SPSA
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import TwoLocal
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA, L_BFGS_B, SLSQP
from qiskit.circuit.library import EfficientSU2
from qiskit.primitives import Sampler, Estimator
from qiskit_algorithms.state_fidelities import ComputeUncompute
from qiskit_algorithms.utils import algorithm_globals
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_algorithms import VQD



ansatz = EfficientSU2(qubit_jw_op.num_qubits, reps=2)
optimizer = SLSQP()
estimator = Estimator()
sampler = Sampler()
fidelity = ComputeUncompute(sampler)


QiskitRuntimeService.save_account(channel='ibm_quantum', token='2cf504094070e6aa12cea3b83a6d0d2e31aabe3fe4880fe0f1d645c589b879158c9a704f5cff5135093067e4a731a56611ffdbb8ff6704f11cc61fb309eb7592', overwrite=True)
service = QiskitRuntimeService()

counts = []
values = []
steps = []

def callback(eval_count, parameters, value, stddev, *args):
    steps.append(eval_count)
    values.append(value)
    print(f"Step {eval_count}: Value = {value}, Stddev = {stddev}")

k = 3

vqd = VQD(estimator, fidelity, ansatz, optimizer, k=k, callback=callback)
result = vqd.compute_eigenvalues(operator=qubit_jw_op)
vqd_values = result.eigenvalues
print(vqd_values.real)

# for Carbon Monoxide
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper

# Define the PySCFDriver for Carbon Monoxide
driver = PySCFDriver(
    atom="C 0 0 0; O 0 0 1.128",  # Approximate bond length in Angstroms for CO
    basis="6-31g",               # Basis set to use
    charge=0,                    # Neutral molecule
    spin=0,                      # Singlet state (all electrons paired)
    unit=DistanceUnit.ANGSTROM,  # Specify distance unit
)

es_problem = driver.run()

fermionic_op = es_problem.hamiltonian.second_q_op()

mapper = JordanWignerMapper()
qubit_jw_op = mapper.map(fermionic_op)

print(qubit_jw_op)