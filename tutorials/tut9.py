"""
Tutorial 09: Packing separate facts into a combined fact in [ADA]

Run this file from the same folder as ada.py:

    python tutorial_09_packing_combined_facts.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_09_-_Packing_combined_facts.ada

This tutorial builds on Tutorial 08.

Tutorial 08 started with one combined fact and unpacked it:

    Milo is a cat and Milo is hungry

into two separate facts:

    Milo is a cat
    Milo is hungry

Tutorial 09 goes in the other direction.  It starts with two separate facts,
packs them into one combined fact, and then uses a rule whose premise is that
combined fact.
"""

import ada


ada.notebook(name="Tutorial 09 - Packing combined facts", mode="console")

ada.note(
    "Goal: start with two separate facts, pack them into one combined fact, "
    "then use a rule that expects the combined fact."
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
    name="pack separate facts",
)

# These assumptions introduce the small vocabulary for the tutorial.
entity = proof.assume("entity []", name="entity wrapper")
is_cat = proof.assume("[] is a cat", name="cat predicate")
is_hungry = proof.assume("[] is hungry", name="hungry predicate")
should_eat = proof.assume("[] should eat", name="eat predicate")

# Introduce a particular name.
milo = proof.assume("Milo", name="the name Milo")

ada.note("- Step 3: add a rule that expects one combined condition -")

# This rule says:
#
#     if X is both a cat and hungry, then X should eat.
#
# Notice the extra brackets around the two-part condition:
#
#     [[[X] is a cat][[X] is hungry]]
#
# That tells ADA to treat the two facts as one combined premise.
combined_condition_rule = proof.assume(
    "[X][[[X] is a cat][[X] is hungry]]:[[X] should eat]",
    name="cats that are both cat-and-hungry should eat",
)

ada.note("- Step 4: add two separate facts -")

milo_is_a_cat = proof.assume(
    "[entity [Milo]] is a cat",
    name="first separate fact: Milo is a cat",
)

milo_is_hungry = proof.assume(
    "[entity [Milo]] is hungry",
    name="second separate fact: Milo is hungry",
)

ada.note("- Step 5: pack the two facts into one combined fact -")

# A list passed to conclude asks ADA to restate available facts.
# Here we restate two available facts at once, so ADA produces one
# combined statement with two components.
combined_milo_fact = proof.conclude(
    [
        "[entity [Milo]] is a cat",
        "[entity [Milo]] is hungry",
    ],
    name="packed fact: Milo is cat-and-hungry",
)

ada.note("- Step 6: apply the rule to the packed fact -")

# Now the combined condition required by the rule is available.
milo_should_eat = proof.conclude(
    combined_condition_rule,
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
