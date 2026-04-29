"""
Tutorial 07: Deriving a two-premise [ADA] rule

Run this file from the same folder as ada.py:

    python tutorial_07_deriving_a_two_premise_rule.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_07_-_Deriving_a_two_premise_rule.ada

This tutorial builds on Tutorial 06.

Tutorial 06 reused a two-premise rule that was assumed.

Tutorial 07 shows how to derive a two-premise rule from simpler rules.

We start with two simpler rules:

    Milo is a cat
    therefore Milo is an animal

    Milo is an animal
    Milo is hungry
    therefore Milo should eat

From these, a nested argument derives the new rule:

    Milo is a cat
    Milo is hungry
    therefore Milo should eat

Then the main argument uses that derived rule.
"""

import ada


ada.notebook(name="Tutorial 07 - Deriving a two-premise rule", mode="console")

ada.note(
    "Goal: derive a two-premise rule inside a nested argument, "
    "then use the derived rule in the main argument."
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
    name="derive a two-premise rule",
)

# These assumptions introduce the small vocabulary for the tutorial.
entity = main.assume("entity []", name="entity wrapper")
is_cat = main.assume("[] is a cat", name="cat predicate")
is_animal = main.assume("[] is an animal", name="animal predicate")
is_hungry = main.assume("[] is hungry", name="hungry predicate")
should_eat = main.assume("[] should eat", name="eat predicate")

# Introduce the name that this tutorial is about.
milo = main.assume("Milo", name="the name Milo")

ada.note("- Step 3: add two simpler rules -")

# Rule 1: if Milo is a cat, then Milo is an animal.
milo_cat_implies_milo_animal = main.assume(
    "[[entity [Milo]] is a cat]:[[entity [Milo]] is an animal]",
    name="Milo cat implies Milo animal",
)

# Rule 2: if Milo is an animal and Milo is hungry,
# then Milo should eat.
hungry_milo_animals_eat = main.assume(
    "[[entity [Milo]] is an animal][[entity [Milo]] is hungry]:"
    "[[entity [Milo]] should eat]",
    name="hungry Milo animals eat",
)

ada.note("- Step 4: open a nested argument to derive a two-premise rule -")

# To prove the derived rule, temporarily assume its two premises:
#
#     Milo is a cat
#     Milo is hungry
#
# Then derive the conclusion:
#
#     Milo should eat
rule_proof = ada.argument(
    main,
    name="derive: hungry Milo cats should eat",
)

temporary_cat_fact = rule_proof.assume(
    "[entity [Milo]] is a cat",
    name="temporary premise: Milo is a cat",
)

temporary_hungry_fact = rule_proof.assume(
    "[entity [Milo]] is hungry",
    name="temporary premise: Milo is hungry",
)

milo_is_an_animal = rule_proof.conclude(
    milo_cat_implies_milo_animal,
    name="inside rule proof: Milo is an animal",
)

milo_should_eat_inside = rule_proof.conclude(
    hungry_milo_animals_eat,
    name="inside rule proof: Milo should eat",
)

# Closing the nested argument packages the temporary premises and final result
# as a derived two-premise inference.
derived_rule_inside = rule_proof.conclude()

ada.note("- Step 5: return the derived rule to the main argument -")

hungry_milo_cats_should_eat = main.conclude(
    rule_proof,
    name="derived rule: hungry Milo cats should eat",
)

ada.note("- Step 6: add the actual facts in the main argument -")

milo_is_a_cat = main.assume(
    "[entity [Milo]] is a cat",
    name="Milo is a cat",
)

milo_is_hungry = main.assume(
    "[entity [Milo]] is hungry",
    name="Milo is hungry",
)

ada.note("- Step 7: use the derived two-premise rule -")

milo_should_eat = main.conclude(
    hungry_milo_cats_should_eat,
    name="Milo should eat by the derived rule",
)

# Close the main argument. ADA packages the assumptions and final conclusion
# as one larger inference.
concluding_inference = main.conclude()

ada.note("- Step 8: display the packaged results and proof -")
ada.note(derived_rule_inside, "This is the rule packaged by the nested argument.")
ada.note(concluding_inference, "This is the inference proved by the whole argument.")
main.proof("fitch")

ada.save()
