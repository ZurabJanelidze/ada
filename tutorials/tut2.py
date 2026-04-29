"""
Tutorial 02: Chaining two [ADA] inferences

Run this file from the same folder as ada.py:

    python tutorial_02_chaining_inferences.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_02_-_Chaining_inferences.ada

This tutorial builds on Tutorial 01.

Tutorial 01 used one rule:

    cat -> animal

This tutorial uses two rules:

    kitten -> cat
    cat -> animal

So the proof has one intermediate conclusion:

    Milo is a kitten
    therefore Milo is a cat
    therefore Milo is an animal
"""

import ada


ada.notebook(name="Tutorial 02 - Chaining inferences", mode="console")

ada.note(
    "Goal: chain two rules. From 'Milo is a kitten', "
    "'every kitten is a cat', and 'every cat is an animal', "
    "deduce 'Milo is an animal'."
)

ada.note("- Step 1: name the inference pattern -")
_inf_ = ada.note(
    ada.exp("[]:[]"),
    "Read this as: from the left statement, conclude the right statement.",
)

ada.note("- Step 2: build a chained argument -")
proof = ada.argument(theme="fitch", dialect="natural", name="kittens are animals")

# These assumptions introduce the small vocabulary for the tutorial.
entity = proof.assume("entity []", name="entity wrapper")
is_kitten = proof.assume("[] is a kitten", name="kitten predicate")
is_cat = proof.assume("[] is a cat", name="cat predicate")
is_animal = proof.assume("[] is an animal", name="animal predicate")

# Introduce a particular name.
milo = proof.assume("Milo", name="the name Milo")

# Rule 1: for any X, if X is a kitten, then X is a cat.
every_kitten_is_a_cat = proof.assume(
    "[X][[X] is a kitten]:[[X] is a cat]",
    name="every kitten is a cat",
)

# Rule 2: for any X, if X is a cat, then X is an animal.
every_cat_is_an_animal = proof.assume(
    "[X][[X] is a cat]:[[X] is an animal]",
    name="every cat is an animal",
)

# Starting fact.
milo_is_a_kitten = proof.assume(
    "[entity [Milo]] is a kitten",
    name="Milo is a kitten",
)

ada.note("- Step 3: make the intermediate conclusion -")
milo_is_a_cat = proof.conclude(
    every_kitten_is_a_cat,
    "entity [Milo]",
    name="intermediate result: Milo is a cat",
)

ada.note("- Step 4: use the intermediate conclusion to finish -")
milo_is_an_animal = proof.conclude(
    every_cat_is_an_animal,
    "entity [Milo]",
    name="final result: Milo is an animal",
)

# Close the argument. ADA packages the assumptions and final conclusion
# as one larger inference.
concluding_inference = proof.conclude()

ada.note("- Step 5: display the packaged result and proof -")
ada.note(concluding_inference, "This is the inference proved by the argument.")
proof.proof("fitch")

ada.save()
