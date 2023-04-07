from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is a Knight or a Knave but not both
    And(Or(AKnight, AKnave),Not(And(AKnight, AKnave))),
    # The sentence "I am a knight and a knave." is true and A is a knight
    # or the sentence is false
    Or(And(AKnight, And(AKnight, AKnave)),
        And(AKnave, Not(And(AKnight, AKnave))))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is a Knight or a Knave but not both
    And(Or(AKnight, AKnave),Not(And(AKnight, AKnave))),
    # B is a Knight or a Knave but not both
    And(Or(BKnight, BKnave),Not(And(BKnight, BKnave))),
    # A says We are both knaves.
    Or(And(AKnight, And(AKnave, BKnave)),And(AKnave, Not(And(AKnave, BKnave))))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is a Knight or a Knave but not both.
    And(Or(AKnight, AKnave),Not(And(AKnight, AKnave))),
    # B is a Knight or a Knave but not both.
    And(Or(BKnight, BKnave),Not(And(BKnight, BKnave))),
    # A says We are the same kind.
    Or(And(AKnight,     Or(And(AKnight,BKnight), And(AKnave, BKnave))),
        And(AKnave,  Not(Or(And(AKnight,BKnight), And(AKnave, BKnave))))),
    # B says We are different kinds.
    Or(And(BKnight,     Or(And(AKnight,BKnave), And(AKnave, BKnight))),
        And(BKnave,  Not(Or(And(AKnight,BKnave), And(AKnave, BKnight)))))
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
ASaidKnight = Symbol("A said I'm a Knight.")
ASaidKnave = Symbol("A said I am a Knave.")
knowledge3 = And(
    # A is a Knight or a Knave but not both.
    And(Or(AKnight, AKnave),Not(And(AKnight, AKnave))),
    # B is a Knight or a Knave but not both.
    And(Or(BKnight, BKnave),Not(And(BKnight, BKnave))),
    # C is a Knight or a Knave but not both.
    And(Or(CKnight, CKnave),Not(And(CKnight, CKnave))),
    # A said Knight or Knave
    Implication(AKnight, ASaidKnight),
    Implication(AKnave, ASaidKnight),
    And(Or(ASaidKnight, ASaidKnave),Not(And(ASaidKnight, ASaidKnave))),
    # A says either I am a knight or I am a knave but you don't know which.
    # I feel like I need another symbol here for "What A said", I mean, I know
    # no matter whether he's a knight or knave he'll say he's a knight, but
    # I don't see how to code that without another symbol.
    Or(And(AKnight, ASaidKnight), And(AKnave, Not(ASaidKnave))),
    # B says "A said 'I am a knave"
    Or(And(BKnight, ASaidKnave), And(BKnave, Not(ASaidKnave))),
    # B says C is a knave
    Or(And(BKnight, CKnave), And(BKnave, Not(CKnave))),
    # C says A is knight
    Or(And(CKnight, AKnight), And(CKnave, Not(AKnight)))
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave, ASaidKnight, ASaidKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
