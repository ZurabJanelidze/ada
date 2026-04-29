
"""
Tutorial 11: Proving symmetry inside a tiny [ADA] theory

Goal:
Build on Tutorial 10's tiny theory of equivalence.

Tutorial 10 introduced:
    propositions,
    equivalence,
    introduction of equivalence,

then proved:
    every proposition is equivalent to itself.

Tutorial 11 adds:
    elimination of equivalence I,
    elimination of equivalence II,

then proves:
    equivalence is symmetric.
"""

import ada

ada.notebook(name="Tutorial 11 - Symmetry of equivalence", mode="console")

ada.note(
    "Goal: extend the tiny equivalence theory from Tutorial 10 and prove "
    "that equivalence is symmetric."
)

ada.note("- Step 1: recall the inference pattern -")
_inf_ = ada.note(
    ada.exp("[]:[]"),
    "Read this as: from the left statement, conclude the right statement.",
)

X = ada.exp("X")
Y = ada.exp("Y")
Z = ada.exp("Z []")
F = ada.exp("F []")
G = ada.exp("G []")

ada.note("- Step 2: restart the tiny theory of equivalence -")
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

ada.note("- Step 3: recall Tutorial 10's theorem: reflexivity -")
reflexive_proof = ada.argument(
    equivalence,
    name="prove equivalence reflexive",
    theme="hidden",
    dialect="natural",
)

reflexive_proof.assume(Z)

forward = ada.argument(reflexive_proof)
forward.assume(Z(istrue))
forward.conclude([Z(istrue)])
forward.conclude()

reflexive_proof.conclude(forward)
reflexive_proof.conclude(intro_equiv, Z(istrue), Z(istrue))
reflexive_proof.conclude()

reflexivity = equivalence.conclude(reflexive_proof)
reflexive_proof.proof("fitch")

ada.note("- Step 4: add two elimination rules for equivalence -")

elim_equiv_i = equivalence.assume(
    _inf_((X, Y, _equiv_(X, Y)), _inf_(X, Y)),
    name="elimination of equivalence I",
)

elim_equiv_ii = equivalence.assume(
    _inf_((X, Y, _equiv_(X, Y)), _inf_(Y, X)),
    name="elimination of equivalence II",
)

ada.note("- Step 5: prove symmetry of equivalence -")

symmetry_proof = ada.argument(
    equivalence,
    name="prove equivalence symmetric",
    theme="hidden",
    dialect="natural",
)

# Temporarily assume two proposition forms F and G, and the fact that
# F is equivalent to G.
symmetry_proof.assume(F, G, _equiv_(F(istrue), G(istrue)))

# From F <=> G, equivalence elimination gives F => G.
f_implies_g = symmetry_proof.conclude(
    elim_equiv_i,
    F(istrue),
    G(istrue),
    name="F implies G",
)

# From F <=> G, equivalence elimination also gives G => F.
g_implies_f = symmetry_proof.conclude(
    elim_equiv_ii,
    F(istrue),
    G(istrue),
    name="G implies F",
)

# To prove G <=> F, use equivalence introduction.
# Its two required directions are:
#
#     G => F
#     F => G
symmetry_proof.conclude(
    intro_equiv,
    G(istrue),
    F(istrue),
    name="G is equivalent to F",
)

symmetry_proof.conclude()

symmetry = equivalence.conclude(symmetry_proof)
symmetry_proof.proof("fitch")

ada.save()
