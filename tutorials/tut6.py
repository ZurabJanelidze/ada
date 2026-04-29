"""
Tutorial 06: Reusing a general two-premise [ADA] rule

Run this file from the same folder as ada.py:

    python tutorial_06_reusing_general_rule.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_06_-_Reusing_general_rule.ada

This tutorial builds on Tutorial 05.

Tutorial 05 used a two-premise rule about Milo only:

    Milo is a cat
    Milo is hungry
    therefore Milo should eat

Tutorial 06 makes that rule general:

    X is a cat
    X is hungry
    therefore X should eat

Then it reuses the same rule twice:

    once for Milo
    once for Luna
"""

import ada


ada.notebook(name="Tutorial 06 - Reusing general rule", mode="console")

ada.note(
    "Goal: make the two-premise rule general, then use the same rule "
    "for two different names."
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
    name="reuse a general two-premise rule",
)

# These assumptions introduce the small vocabulary for the tutorial.
entity = proof.assume("entity []", name="entity wrapper")
is_cat = proof.assume("[] is a cat", name="cat predicate")
is_hungry = proof.assume("[] is hungry", name="hungry predicate")
should_eat = proof.assume("[] should eat", name="eat predicate")

ada.note("- Step 3: add one general rule -")

# This rule has a placeholder X and two required facts:
#
#     [X] is a cat
#     [X] is hungry
#
# Its conclusion is:
#
#     [X] should eat
#
# The leading [X] tells ADA that X is the part we will later replace.
general_two_premise_rule = proof.assume(
    "[X][[X] is a cat][[X] is hungry]:[[X] should eat]",
    name="hungry cats should eat",
)

ada.note("- Step 4: add facts about Milo -")

milo = proof.assume("Milo", name="the name Milo")

milo_is_a_cat = proof.assume(
    "[entity [Milo]] is a cat",
    name="Milo is a cat",
)

milo_is_hungry = proof.assume(
    "[entity [Milo]] is hungry",
    name="Milo is hungry",
)

ada.note("- Step 5: apply the general rule to Milo -")

milo_should_eat = proof.conclude(
    general_two_premise_rule,
    "entity [Milo]",
    name="Milo should eat",
)

ada.note("- Step 6: add facts about Luna -")

luna = proof.assume("Luna", name="the name Luna")

luna_is_a_cat = proof.assume(
    "[entity [Luna]] is a cat",
    name="Luna is a cat",
)

luna_is_hungry = proof.assume(
    "[entity [Luna]] is hungry",
    name="Luna is hungry",
)

ada.note("- Step 7: reuse the same general rule for Luna -")

luna_should_eat = proof.conclude(
    general_two_premise_rule,
    "entity [Luna]",
    name="Luna should eat",
)

# Close the argument. ADA packages the assumptions and final conclusion
# as one larger inference.
concluding_inference = proof.conclude()

ada.note("- Step 8: display the packaged result and proof -")
ada.note(concluding_inference, "This is the inference proved by the argument.")
proof.proof("fitch")

ada.save()
