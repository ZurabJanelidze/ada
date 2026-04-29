"""
Tutorial 08: Unpacking a combined fact in [ADA]

Run this file from the same folder as ada.py:

    python tutorial_08_unpacking_combined_facts.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_08_-_Unpacking_combined_facts.ada

This tutorial builds on Tutorial 07.

Tutorial 07 used two separate facts:

    Milo is a cat
    Milo is hungry

Tutorial 08 starts with one combined fact instead:

    Milo is a cat and Milo is hungry

Then it restates each part separately, so a two-premise rule can use them:

    Milo is a cat
    Milo is hungry
    therefore Milo should eat

The new idea is that a single [ADA] statement may contain several components.
A proof may restate the needed components when they are already available
inside the current argument.
"""

import ada


ada.notebook(name="Tutorial 08 - Unpacking combined facts", mode="console")

ada.note(
    "Goal: start with one combined fact, unpack its two parts, "
    "then apply a two-premise rule."
)

ada.note("- Step 1: recall the inference pattern -")
_inf_ = ada.note(
    ada.exp("[]:[]"),
    "Read this as: from the left statement, conclude the right statement.",
)

ada.note("- Step 2: start the argument -")
proof = ada.argument(
    theme="fitch",
    dialect="natural",
    name="unpack a combined fact",
)

# These assumptions introduce the small vocabulary for the tutorial.
entity = proof.assume("entity []", name="entity wrapper")
is_cat = proof.assume("[] is a cat", name="cat predicate")
is_hungry = proof.assume("[] is hungry", name="hungry predicate")
should_eat = proof.assume("[] should eat", name="eat predicate")

# Introduce a particular name.
milo = proof.assume("Milo", name="the name Milo")

ada.note("- Step 3: add one combined fact -")

# This is one assumption with two components:
#
#     [[entity [Milo]] is a cat]
#     [[entity [Milo]] is hungry]
#
# ADA displays this naturally as:
#
#     (entity Milo) is a cat, (entity Milo) is hungry
combined_milo_fact = proof.assume(
    "[[entity [Milo]] is a cat][[entity [Milo]] is hungry]",
    name="combined fact: Milo is a cat and hungry",
)

ada.note("- Step 4: restate each component separately -")

# Because the two parts are already present inside the combined fact,
# ADA can restate each part as its own line.
milo_is_a_cat = proof.conclude(
    ["[entity [Milo]] is a cat"],
    name="unpacked part 1: Milo is a cat",
)

milo_is_hungry = proof.conclude(
    ["[entity [Milo]] is hungry"],
    name="unpacked part 2: Milo is hungry",
)

ada.note("- Step 5: add a general two-premise rule -")

# This is the same kind of general rule used in Tutorial 06:
#
#     X is a cat
#     X is hungry
#     therefore X should eat
hungry_cats_should_eat = proof.assume(
    "[X][[X] is a cat][[X] is hungry]:[[X] should eat]",
    name="hungry cats should eat",
)

ada.note("- Step 6: apply the rule after unpacking the fact -")

# The required two facts are now available as separate proof lines,
# so the two-premise rule can be applied to Milo.
milo_should_eat = proof.conclude(
    hungry_cats_should_eat,
    "entity [Milo]",
    name="Milo should eat",
)

# Close the argument. ADA packages the assumptions and final conclusion
# as one larger inference.
concluding_inference = proof.conclude()

ada.note("- Step 7: display the packaged result and proof -")
ada.note(concluding_inference, "This is the inference proved by the argument.")
proof.proof("fitch")

ada.save()
