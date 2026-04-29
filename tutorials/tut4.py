"""
Tutorial 04: Proving and using a derived [ADA] rule

Run this file from the same folder as ada.py:

    python tutorial_04_derived_rule.py

It will print an [ADA] notebook to the console and save a notebook file:

    Tutorial_04_-_Derived_rule.ada

This tutorial builds on Tutorial 03.

Tutorial 03 used a nested argument to prove a small claim.

Tutorial 04 uses a nested argument to prove a new rule:

    If Milo is a kitten, then Milo is an animal.

After the rule is proved, the main argument uses it just like any other rule.
"""

import ada


ada.notebook(name="Tutorial 04 - Derived rule", mode="console")

ada.note(
    "Goal: prove a new rule inside a nested argument, then use the new rule "
    "in the main argument."
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
    name="derive and use a rule",
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

ada.note("- Step 3: open a nested argument to prove a new rule -")

# To prove "if Milo is a kitten, then Milo is an animal",
# temporarily assume the premise, then derive the conclusion.
rule_proof = ada.argument(main, name="derive: Milo kitten implies Milo animal")

temporary_premise = rule_proof.assume(
    "[entity [Milo]] is a kitten",
    name="temporary premise",
)

milo_is_a_cat = rule_proof.conclude(
    every_kitten_is_a_cat,
    "entity [Milo]",
    name="inside rule proof: Milo is a cat",
)

milo_is_an_animal_inside = rule_proof.conclude(
    every_cat_is_an_animal,
    "entity [Milo]",
    name="inside rule proof: Milo is an animal",
)

# Closing the nested argument packages the temporary premise and the final
# result as a derived inference:
#
#     [entity [Milo]] is a kitten : [entity [Milo]] is an animal
derived_rule_inside = rule_proof.conclude()

ada.note("- Step 4: return the derived rule to the main argument -")

derived_rule = main.conclude(
    rule_proof,
    name="derived rule: Milo kitten implies Milo animal",
)

ada.note("- Step 5: use the derived rule -")

# Now we add the actual fact in the main argument.
milo_is_a_kitten = main.assume(
    "[entity [Milo]] is a kitten",
    name="Milo is a kitten",
)

# Since the derived rule is now available in the main argument,
# ADA can use it to conclude that Milo is an animal.
milo_is_an_animal = main.conclude(
    derived_rule,
    name="Milo is an animal by the derived rule",
)

# Close the main argument.
concluding_inference = main.conclude()

ada.note("- Step 6: display the packaged results and proof -")
ada.note(derived_rule_inside, "This is the rule packaged by the nested argument.")
ada.note(concluding_inference, "This is the inference proved by the whole argument.")
main.proof("fitch")

ada.save()
