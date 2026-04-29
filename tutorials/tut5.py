"""
Tutorial 05: Using a rule with two premises in [ADA]

Run this file from the same folder as ada.py:

    python tutorial_05_two_premise_rule.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_05_-_Two_premise_rule.ada

This tutorial builds on Tutorial 04.

Tutorial 04 proved and used a derived rule with one premise:

    Milo is a kitten
    therefore Milo is an animal

Tutorial 05 introduces a rule that needs two premises:

    Milo is a cat
    Milo is hungry
    therefore Milo should eat

The new idea is that the left side of an inference can contain more than
one statement.
"""

import ada


ada.notebook(name="Tutorial 05 - Two premise rule", mode="console")

ada.note(
    "Goal: use a rule that requires two facts before it can be applied."
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
    name="a rule with two premises",
)

# These assumptions introduce the small vocabulary for the tutorial.
entity = proof.assume("entity []", name="entity wrapper")
is_cat = proof.assume("[] is a cat", name="cat predicate")
is_hungry = proof.assume("[] is hungry", name="hungry predicate")
should_eat = proof.assume("[] should eat", name="eat predicate")

# Introduce a particular name.
milo = proof.assume("Milo", name="the name Milo")

ada.note("- Step 3: add a rule with two premises -")

# The premise side of this rule is the concatenation of two statements:
#
#     [[entity [Milo]] is a cat][[entity [Milo]] is hungry]
#
# ADA reads this naturally as:
#
#     (entity Milo) is a cat and (entity Milo) is hungry
#
# The conclusion side is:
#
#     [[entity [Milo]] should eat]
two_premise_rule = proof.assume(
    "[[entity [Milo]] is a cat][[entity [Milo]] is hungry]:"
    "[[entity [Milo]] should eat]",
    name="cats that are hungry should eat",
)

ada.note("- Step 4: add both required facts -")

milo_is_a_cat = proof.assume(
    "[entity [Milo]] is a cat",
    name="first premise: Milo is a cat",
)

milo_is_hungry = proof.assume(
    "[entity [Milo]] is hungry",
    name="second premise: Milo is hungry",
)

ada.note("- Step 5: apply the two-premise rule -")

# Because both required facts are now available, ADA can apply the rule.
milo_should_eat = proof.conclude(
    two_premise_rule,
    name="Milo should eat",
)

# Close the argument. ADA packages the assumptions and final conclusion
# as one larger inference.
concluding_inference = proof.conclude()

ada.note("- Step 6: display the packaged result and proof -")
ada.note(concluding_inference, "This is the inference proved by the argument.")
proof.proof("fitch")

ada.save()
