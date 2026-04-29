"""
Tutorial 12: Homomorphic unitary magmas are commutative monoids

Run this file from the same folder as ada.py:

    python tutorial_13_commutative_monoid.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_13_-_Homomorphic_unitary_magmas.ada

This tutorial builds on Tutorial 12.

Tutorial 12 introduced equality substitution.

Here we use equality substitution in a less toy-like algebraic proof.

Mathematical goal:
    A unitary magma whose operation is a homomorphism is necessarily
    a commutative monoid.

The homomorphism condition for the operation is written as the interchange law:

    (a*b)*(c*d) = (a*c)*(b*d)

The unitary magma assumptions give:

    unit*x = x
    x*unit = x

From these, we prove:
    associativity:   (x*y)*z = x*(y*z)
    commutativity:   x*y = y*x

Together with the assumed two-sided unit laws, these are the laws of a
commutative monoid.
"""

import ada


# The current development version of ada.py prints an internal debug message
# during equality substitution. This line keeps the tutorial output clean.
ada.pr = lambda *inputs: None


ada.notebook(name="Tutorial 13 - Homomorphic unitary magmas", mode="console")

ada.note(
    "Goal: prove that a unitary magma whose operation is a homomorphism "
    "has the laws of a commutative monoid."
)

ada.note("- Step 1: recall the inference pattern -")
_inf_ = ada.note(
    ada.exp("[]:[]"),
    "Read this as: from the left statement, conclude the right statement.",
)
_equal_ = ada.note(
    ada.exp("[]=[]"),
    "Use this to state equality of two things"
)

ada.note("- Step 2: choose variables for the tutorial -")

# These are the variables used in the final theorems.
x = ada.exp("x[]")
y = ada.exp("y[]")
z = ada.exp("z[]")

# These are schema variables used in the general axioms.
a = ada.exp("a[]")
b = ada.exp("b[]")
c = ada.exp("c[]")
d = ada.exp("d[]")

ada.note("- Step 3: start the algebraic theory -")

magma = ada.argument(
    theme="theory",
    name="unitary homomorphic magma",
    dialect="natural",
)

# Vocabulary.
_op_ = magma.assume("[] . []", name="magma operation")
ent = magma.assume("_", name="entity marker")
unit = magma.assume("1[]", name="unit element name")

ada.note("- Step 4: state the unit laws -")

# A unitary magma has a left unit and a right unit.
left_unit = magma.assume(
    _inf_(a, _equal_(_op_(unit(ent), a(ent)), a(ent))),
    name="left unit law",
)

right_unit = magma.assume(
    _inf_(a, _equal_(_op_(a(ent), unit(ent)), a(ent))),
    name="right unit law",
)

ada.note("- Step 5: state that the operation is a homomorphism -")

# The operation is a homomorphism precisely when it preserves the magma
# operation on pairs.  In element notation this is the interchange law:
#
#     (a*b)*(c*d) = (a*c)*(b*d)
interchange = magma.assume(
    _inf_(
        (a, b, c, d),
        _equal_(
            _op_(_op_(a(ent), b(ent)), _op_(c(ent), d(ent))),
            _op_(_op_(a(ent), c(ent)), _op_(b(ent), d(ent))),
        ),
    ),
    name="operation homomorphism / interchange law",
)

ada.note("- Step 6: prove associativity -")

assoc_proof = ada.argument(
    magma,
    name="prove associativity",
    #theme="hidden",
    dialect="natural",
    theme="narrative",
)

# Temporarily reserve the variables x, y, and z.  This keeps ADA from
# renaming them during equality substitutions.
assoc_proof.assume(x, y, z)

# Start from the interchange law with a=x, b=y, c=unit, d=z:
#
#     (x*y)*(unit*z) = (x*unit)*(y*z)
left_z = assoc_proof.conclude(
    left_unit,
    z(ent),
    name="unit*z = z",
)

right_x = assoc_proof.conclude(
    right_unit,
    x(ent),
    name="x*unit = x",
)

interchange_assoc = assoc_proof.conclude(
    interchange,
    x(ent),
    y(ent),
    unit(ent),
    z(ent),
    name="interchange at x,y,unit,z",
)

# Replace unit*z by z.
assoc_step_1 = assoc_proof.conclude(
    left_z,
    interchange_assoc,
    name="replace unit*z by z",
)

# Replace x*unit by x.
associative_law = assoc_proof.conclude(
    right_x,
    assoc_step_1,
    name="replace x*unit by x",
)

assoc_proof.conclude()

associativity = magma.conclude(assoc_proof)
assoc_proof.proof("fitch")

ada.note("- Step 7: prove commutativity -")

comm_proof = ada.argument(
    magma,
    name="prove commutativity",
    theme="narrative",
    dialect="natural",
)

# Reserve x and y for the final commutativity statement.
comm_proof.assume(x, y)

# Start from the interchange law with a=unit, b=x, c=y, d=unit:
#
#     (unit*x)*(y*unit) = (unit*y)*(x*unit)
left_x = comm_proof.conclude(
    left_unit,
    x(ent),
    name="unit*x = x",
)

right_y = comm_proof.conclude(
    right_unit,
    y(ent),
    name="y*unit = y",
)

left_y = comm_proof.conclude(
    left_unit,
    y(ent),
    name="unit*y = y",
)

right_x_again = comm_proof.conclude(
    right_unit,
    x(ent),
    name="x*unit = x",
)

interchange_comm = comm_proof.conclude(
    interchange,
    unit(ent),
    x(ent),
    y(ent),
    unit(ent),
    name="interchange at unit,x,y,unit",
)

# Substitute each unit law into the interchange equality.
comm_step_1 = comm_proof.conclude(
    left_x,
    interchange_comm,
    name="replace unit*x by x",
)

comm_step_2 = comm_proof.conclude(
    right_y,
    comm_step_1,
    name="replace y*unit by y",
)

comm_step_3 = comm_proof.conclude(
    left_y,
    comm_step_2,
    name="replace unit*y by y",
)

commutative_law = comm_proof.conclude(
    right_x_again,
    comm_step_3,
    name="replace x*unit by x",
)

comm_proof.conclude()

commutativity = magma.conclude(comm_proof)
comm_proof.proof("fitch")

ada.save()
