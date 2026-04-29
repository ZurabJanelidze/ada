# Tutorial 13: Arithmetic in [ADA]

import ada

# Start an [ADA] notebook.  The notebook is the text output produced while the
# proof is assembled.
ada.notebook("Arithmetic")

# Open a theory called "arithmetic".  Assumptions made in this argument become
# the primitive vocabulary, definitions, and axioms of the theory.
arithmetic = ada.argument(theme="theory", name="arithmetic", dialect="natural")

# The expression []:[] is ADA's inference pattern:
#     assumptions on the left  :  conclusion on the right
#
# The call to ada.note both displays the pattern in the notebook and returns it
# so that we can use it as the constructor _inf_ below.
_inf_=ada.note(ada.exp("[]:[]"), "Abbreviated as: {\_}inf{\_}")

# X and Y are schematic expressions for arbitrary statements.
X=ada.exp("X")
Y=ada.exp("Y")

# x[] and y[] are unary expression templates.  Later, x(ent) and y(ent) are used
# as arbitrary entities of the arithmetic theory.
x=ada.exp("x[]")
y=ada.exp("y[]")

# F [] and G [] are unary statement-building templates.  They let us state
# general rules about arbitrary predicates or propositions.
F=ada.exp("F []")
G=ada.exp("G []")

# ---------------------------------------------------------------------------
# Vocabulary of the theory
# ---------------------------------------------------------------------------
#
# These assumptions introduce the pieces of language used in the later axioms.
# Each assigned variable is a constructor that can be applied to expressions.
istrue = arithmetic.assume("is true", name="is true")
_equiv_ = arithmetic.assume("[] <=> []", name="equivalence")
_equal_ = arithmetic.assume("[] = []", name="equality")
false_ = arithmetic.assume("false []", name="fallacy")
_isfalse = arithmetic.assume("[] is false", name="negation")
ent = arithmetic.assume("'", name="entity")
zero_ = arithmetic.assume("0[]", name="zero")
_isnat = arithmetic.assume("[] is a natural number", name="is a number")
_suc = arithmetic.assume("[]+1", name="successor")

# ---------------------------------------------------------------------------
# Logical definitions and rules
# ---------------------------------------------------------------------------

# Equivalence introduction:
# if X implies Y and Y implies X, then X and Y are equivalent.
introEquiv = arithmetic.assume(_inf_((X,Y,_inf_(X,Y),_inf_(Y,X)),_equiv_(X,Y)), name="introduction of equivalence")

# Equivalence elimination I:
# from X <=> Y, we may use the implication X -> Y.
elimEquivI = arithmetic.assume(_inf_((X,Y,_equiv_(X,Y)),_inf_(X,Y)), name="elimination of equivalence I")

# Equivalence elimination II:
# from X <=> Y, we may use the implication Y -> X.
elimEquivII = arithmetic.assume(_inf_((X,Y,_equiv_(X,Y)),_inf_(Y,X)), name="elimination of equivalence II")

# Equality is defined by substitutability:
# X = Y means that every predicate F has the same truth value on X and Y.
defEq = arithmetic.assume(_inf_((X,Y),_equiv_(_equal_(X,Y),_inf_((F,G),_equiv_(F(X),F(Y))))), name="definition of equality")

# Fallacy is the always-available contradiction pattern.
defFallacy = arithmetic.assume(_equiv_(false_(istrue),_inf_(X,X)), name="definition of fallacy")

# Negation is defined by implication to fallacy:
# X is false exactly when X implies false.
defNeg = arithmetic.assume(_inf_(X,_equiv_(_isfalse(X),_inf_(X,false_(istrue)))), name="definition of negation")

# ---------------------------------------------------------------------------
# Arithmetic axioms
# ---------------------------------------------------------------------------

# 0 is a natural number.
zeroNum = arithmetic.assume(_isnat(zero_(ent)), name="zero is a natural number")

# If x is a natural number, then x+1 is a natural number.
sucNum = arithmetic.assume(_inf_((x,_isnat(x(ent))),(_isnat(_suc(x(ent))))), name="successor of a natural number is a natural number")

# 0 is not the successor of any natural number.
arithI = arithmetic.assume(_inf_((x,_isnat(x(ent))),_isfalse(_equal_(zero_(ent),_suc(x(ent))))), name="zero is not a successor of another natural number")

# Successor is injective:
# if x+1 = y+1, then x = y.
arithII = arithmetic.assume(_inf_((x,y,_isnat(x(ent)),_isnat(y(ent))),_inf_(_equal_(_suc(x(ent)),_suc(y(ent))),_equal_(x(ent),y(ent)))), name="successor is injective")

# Induction principle:
# if a property F holds at 0 and is preserved by successor, then it holds for
# every natural number.
arithIII = arithmetic.assume(_inf_((F,F(zero_(ent)),_inf_((x,_isnat(x(ent)),F(x(ent))),F(_suc(x(ent))))),_inf_((x,_isnat(x(ent))),F(x(ent)))), name="induction principle")

# ---------------------------------------------------------------------------
# Derived rule: use X <=> Y together with X to conclude Y
# ---------------------------------------------------------------------------
#
# This packages a common two-step use of equivalence elimination I:
#     X <=> Y gives X -> Y,
#     and X then gives Y.
E = ada.argument(arithmetic,theme="hidden", dialect="natural")
E.assume(F,G,F(istrue),_equiv_(F(istrue),G(istrue)))
EE = E.conclude(elimEquivI, F(istrue), G(istrue))
E.conclude(EE)
E.conclude()

elimEquivIII = arithmetic.conclude(E)
E.proof()

# ---------------------------------------------------------------------------
# Derived rule: use X <=> Y together with Y to conclude X
# ---------------------------------------------------------------------------
#
# This is the symmetric version, using equivalence elimination II.
E = ada.argument(arithmetic,theme="hidden", dialect="natural")
E.assume(F,G,G(istrue),_equiv_(F(istrue),G(istrue)))
EE = E.conclude(elimEquivII, F(istrue), G(istrue))
E.conclude(EE)
E.conclude()

elimEquivIV = arithmetic.conclude(E)
E.proof()

# ---------------------------------------------------------------------------
# Derived rule: contradiction from F and "F is false"
# ---------------------------------------------------------------------------
#
# The definition of negation turns "F is false" into the implication
# F -> false.  Applying that implication to F gives false.
E = ada.argument(arithmetic,theme="hidden", dialect="natural")
E.assume(F,F(istrue),_isfalse(F(istrue)))
E.conclude(defNeg, F(istrue))
EE=E.conclude(elimEquivIII, _isfalse(F(istrue)), _inf_(F(istrue),false_(istrue)))
E.conclude(EE)
E.conclude()

introFalseI = arithmetic.conclude(E)
E.proof()

# ---------------------------------------------------------------------------
# Derived rule: introduce "F is false" from an implication F -> false
# ---------------------------------------------------------------------------
#
# This is the other direction of the definition of negation.
E = ada.argument(arithmetic,theme="hidden", dialect="natural")
E.assume(F,_inf_(F(istrue),false_(istrue)))
E.conclude(defNeg, F(istrue))
EE=E.conclude(elimEquivII, _isfalse(F(istrue)),_inf_(F(istrue),false_(istrue)))
E.conclude(EE)
E.conclude()

introIsFalse = arithmetic.conclude(E)
E.proof()

# ---------------------------------------------------------------------------
# Derived rule: transfer falsity backwards along an implication
# ---------------------------------------------------------------------------
#
# If G implies F, and F is false, then G is false.
# The nested argument D assumes G, derives F, derives false, and therefore
# proves G -> false.  Then introIsFalse turns that into "G is false".
E = ada.argument(arithmetic,theme="hidden", dialect="natural")
E.assume(G, F,_inf_(G(istrue),F(istrue)),_isfalse(F(istrue)))
D = ada.argument(E)
D.assume(G(istrue))
D.conclude(_inf_(G(istrue),F(istrue)))
D.conclude(introFalseI, F(istrue))
D.conclude()
E.conclude(D)
E.conclude(introIsFalse, G(istrue))
E.conclude()

inferIsFalse = arithmetic.conclude(E)
E.proof()

# ---------------------------------------------------------------------------
# Main theorem: every natural number is different from its successor
# ---------------------------------------------------------------------------
#
# The proof is by induction on the property:
#     P(n) := n = n+1 is false
#
# Base case:
# arithI with x = 0 gives 0 = 0+1 is false.
E = ada.argument(arithmetic,theme="hidden", dialect="natural")
E.conclude(arithI, zero_(ent))

# Induction step:
# assume x is natural and P(x), namely x = x+1 is false.
# We must prove P(x+1), namely x+1 = (x+1)+1 is false.
A = ada.argument(E)
A.assume(x,_isnat(x(ent)))
A.assume(_isfalse(_equal_(x(ent),_suc(x(ent)))))

# x+1 is natural, so it can be used as the second natural number in arithII.
A.conclude(sucNum,x(ent))

# If x+1 = (x+1)+1, successor injectivity gives x = x+1.
A.conclude(arithII, x(ent), _suc(x(ent)))

# Since x = x+1 is false, the previous implication lets us infer that
# x+1 = (x+1)+1 is false.
A.conclude(inferIsFalse, _equal_(_suc(x(ent)),_suc(_suc(x(ent)))), _equal_(x(ent),_suc(x(ent))))

# Close the induction-step subargument.
A.conclude()
E.conclude(A)

# Apply induction to P(n) := n = n+1 is false.
#
# The expression below is the predicate template supplied to ADA's induction
# axiom.  The two empty slots mark where the current natural number is inserted.
E.conclude(arithIII, [_isfalse(_equal_("",_suc(""))),[1,1]])
E.conclude()

# Add the completed theorem to the arithmetic theory and display the proof.
arithmetic.conclude(E)
E.proof("fitch")
