"""
Tutorial 10: Starting a theory in [ADA]

Goal:
Build a tiny theory of equivalence.

We introduce:
    propositions,
    equivalence,
    equivalence introduction,
    equivalence elimination,

then prove:
    every proposition is equivalent to itself.
"""

import ada

ada.notebook(name="Tutorial 10 - Starting a theory", mode="console")

ada.note("Goal: build a tiny theory and prove a theorem inside it.")

_inf_ = ada.note(
    ada.exp("[]:[]"),
    "Read this as: from the left statement, conclude the right statement.",
)

X = ada.exp("X")
Y = ada.exp("Y")
Z = ada.exp("Z []")

equivalence = ada.argument(
    theme="theory",
    name="equivalence",
    dialect="natural",
)

istrue = equivalence.assume(
    "is true",
    name="proposition formulator",
)

_equiv_ = equivalence.assume(
    "[] <=> []",
    name="equivalence formulator",
)

intro_equiv = equivalence.assume(
    _inf_((X, Y, _inf_(X, Y), _inf_(Y, X)), _equiv_(X, Y)),
    name="introduction of equivalence",
)

ada.note("- Prove reflexivity of equivalence -")

proof = ada.argument(
    equivalence,
    name="prove equivalence reflexive",
    theme="hidden",
    dialect="natural",
)

proof.assume(Z)

forward = ada.argument(proof)
forward.assume(Z(istrue))
forward.conclude([Z(istrue)])
forward.conclude()

proof.conclude(forward)
proof.conclude(intro_equiv, Z(istrue), Z(istrue))
proof.conclude()

reflexivity = equivalence.conclude(proof)
proof.proof("fitch")

ada.save()
