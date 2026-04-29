"""
Tutorial 03: Nested [ADA] arguments

Run this file from the same folder as ada.py:

    python tutorial_03_nested_arguments.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_03_-_Nested_arguments.ada

This tutorial builds on Tutorial 02.

Tutorial 02 chained two rules in one argument:

    kitten -> cat
    cat -> animal

This tutorial puts the chained reasoning inside a nested argument.
The nested argument proves a small claim:

    Milo is an animal

Then the main argument brings that claim back into its own proof.
"""

import ada


ada.notebook(name="Tutorial 03 - Nested arguments", mode="console")

ada.note(
    "Goal: use a nested argument to prove the small claim "
    "'Milo is an animal', then return that claim to the main argument."
)

ada.note("- Step 1: recall the inference pattern -")
_inf_ = ada.note(
    ada.exp("[]:[]"),
    "Read this as: from the left statement, conclude the right statement.",
)

ada.note("- Step 2: start the main argument -")
main = ada.argument(
    theme="fitch",
    dialect="natural",
    name="main argument with a nested claim",
)

# These assumptions introduce the small vocabulary for the tutorial.
entity = main.assume("entity []", name="entity wrapper")
is_kitten = main.assume("[] is a kitten", name="kitten predicate")
is_cat = main.assume("[] is a cat", name="cat predicate")
is_animal = main.assume("[] is an animal", name="animal predicate")

# Introduce a particular name.
milo = main.assume("Milo", name="the name Milo")

# Rule 1: for any X, if X is a kitten, then X is a cat.
every_kitten_is_a_cat = main.assume(
    "[X][[X] is a kitten]:[[X] is a cat]",
    name="every kitten is a cat",
)

# Rule 2: for any X, if X is a cat, then X is an animal.
every_cat_is_an_animal = main.assume(
    "[X][[X] is a cat]:[[X] is an animal]",
    name="every cat is an animal",
)

# Starting fact.
milo_is_a_kitten = main.assume(
    "[entity [Milo]] is a kitten",
    name="Milo is a kitten",
)

ada.note("- Step 3: open a nested argument for a small claim -")

# A nested argument has access to the assumptions and conclusions
# already available in the main argument.
claim = ada.argument(main, name="claim: Milo is an animal")

# Inside the claim, we repeat the two-step chain from Tutorial 02.
milo_is_a_cat = claim.conclude(
    every_kitten_is_a_cat,
    "entity [Milo]",
    name="inside claim: Milo is a cat",
)

milo_is_an_animal = claim.conclude(
    every_cat_is_an_animal,
    "entity [Milo]",
    name="inside claim: Milo is an animal",
)

# Close the nested argument. Its final conclusion is packaged.
closed_claim = claim.conclude()

ada.note("- Step 4: return the claim to the main argument -")

# The main argument can now cite the completed nested argument.
returned_claim = main.conclude(
    claim,
    name="claim returned to the main argument",
)

# Close the main argument.
concluding_inference = main.conclude()

ada.note("- Step 5: display the packaged results and proof -")
ada.note(closed_claim, "This is the result packaged by the nested argument.")
ada.note(concluding_inference, "This is the inference proved by the whole argument.")
main.proof("fitch")

ada.save()
