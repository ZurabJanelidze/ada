"""
Tutorial 01: A first [ADA] proof

Run this file from the same folder as ada.py:

    python tutorial_01_basic_proof.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_01_-_A_first_proof.ada
"""

import ada


ada.notebook(name="Tutorial 01 - A first proof", mode="console")

ada.note(
    "Goal: from 'Milo is a cat' and 'every cat is an animal', "
    "deduce 'Milo is an animal'."
)

ada.note("- Step 1: name the inference pattern -")
_inf_ = ada.note(
    ada.exp("[]:[]"),
    "Read this as: from the left statement, conclude the right statement.",
)

ada.note("- Step 2: build a short argument -")
proof = ada.argument(theme="fitch", dialect="natural", name="cats are animals")

# These first three assumptions introduce the pieces of language used below.
entity = proof.assume("entity []", name="entity wrapper")
is_cat = proof.assume("[] is a cat", name="cat predicate")
is_animal = proof.assume("[] is an animal", name="animal predicate")

# We introduce a name.
milo = proof.assume("Milo", name="the name Milo")

# A general rule: for any X, if X is a cat, then X is an animal.
every_cat_is_an_animal = proof.assume(
    "[X][[X] is a cat]:[[X] is an animal]",
    name="every cat is an animal",
)

# A particular fact.
milo_is_a_cat = proof.assume(
    "[entity [Milo]] is a cat",
    name="Milo is a cat",
)

# Apply the rule to the particular entity "Milo".
milo_is_an_animal = proof.conclude(
    every_cat_is_an_animal,
    "entity [Milo]",
    name="Milo is an animal",
)

# Close the argument. ADA packages the assumptions and final conclusion
# as a single inference.
concluding_inference = proof.conclude()

ada.note("- Step 3: display the packaged result and proof -")
ada.note(concluding_inference, "This is the inference proved by the argument.")
proof.proof("fitch")

ada.save()
