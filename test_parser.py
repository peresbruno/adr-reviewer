import sys

sys.path.append("/workspaces/adr-reviewer/src")
from madr_parser.madr_parser import MADRParser

markdown = """# Use Plain JUnit5 for advanced test assertions

## Context and Problem Statement

How to write readable test assertions?
How to write readable test assertions for advanced tests?

## Considered Options

* Plain JUnit5
* Hamcrest
* AssertJ

## Decision Outcome

Chosen option: "Plain JUnit5", because comes out best.

### Consequences

* Good, because tests are more readable
* Good, because more easy to write tests

## Pros and Cons of the Options

### Plain JUnit5

* Good, because Junit5 is "common Java knowledge"
* Bad, because complex assertions tend to get hard to read

### Hamcrest

* Good, because offers advanced matchers
* Bad, because not full fluent API
"""

out = MADRParser.parse(markdown)

print("=" * 60)
print("TITLE:", repr(out.title))
print("=" * 60)
print("CONTEXT:", repr(out.context))
print("=" * 60)
print("DECISION OUTCOME:", repr(out.decision_outcome))
print("=" * 60)
print("CONSIDERED OPTIONS:", out.considered_options)
print("=" * 60)
print("DECISION CONSEQUENCES:", repr(out.decision_consequences))
print("=" * 60)
print("OPTIONS PROS/CONS:", out.options_pros_and_cons)
print("=" * 60)
