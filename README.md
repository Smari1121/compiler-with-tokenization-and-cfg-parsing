# compiler-with-tokenization-and-cfg-parsing
Compiler frontend implementing FSA-based lexical analysis and CFG-based syntactic parsing for a toy programming language, as part of an Automata Theory assignment.

# Compiler Frontend: FSA-Based Tokenization and CFG Parsing

This repository contains a Python implementation of a compiler frontend
for a simple programming language. The focus of this project is on
lexical analysis using Finite State Automata (FSAs) and syntactic
analysis using a Context-Free Grammar (CFG).

The project was developed to demonstrate a clear understanding of
automata theory concepts and their application in real compiler design,
rather than to build a production-ready compiler.

---

## Problem Context

In compiler design, the frontend is responsible for transforming raw
source code into a structured representation that can be analyzed and
validated. This transformation typically occurs in two major stages:

1. **Lexical Analysis (Tokenization)**  
2. **Syntactic Analysis (Parsing)**  

This project implements both stages explicitly from first principles.

---

## Lexical Analysis (Tokenization)

Lexical analysis is performed using **Finite State Automata (FSAs)**.
Each token class is recognized by a deterministic transition system
that reads the source code character by character.

### Token Types Supported
- **Keywords** (e.g., `if`, `else`, `print`)
- **Identifiers**
- **Integers**
- **Floating-point numbers**
- **Symbols and operators**

### Token Hierarchy
When multiple token patterns match the same lexeme, priority is resolved
using a token hierarchy. For example, the string `if` matches the pattern
for identifiers but is correctly classified as a keyword.

Lexical errors such as invalid identifiers (e.g., identifiers starting
with digits) are detected and reported with descriptive error messages.

---

## Syntactic Analysis

After tokenization, the token stream is validated using a
**Context-Free Grammar (CFG)** defined for the language.

The parser checks whether the input program conforms to the grammar
rules and raises syntactic errors when violations are detected (for
example, invalid statement ordering or malformed expressions).

The grammar captures conditional statements, expressions, and nested
statements, enabling the detection of structurally incorrect programs.

---

## Error Handling

The compiler distinguishes clearly between:
- **Lexical errors**: invalid tokens or malformed lexemes
- **Syntactic errors**: grammatically incorrect token sequences

Errors are reported early and precisely to help diagnose the source of
the problem in the input program.

---

## Implementation Overview

- The lexer simulates FSAs directly in Python, without relying on
  regular expression libraries.
- The parser processes the token list sequentially according to the
  grammar rules.
- The design emphasizes clarity, correctness, and conceptual alignment
  with automata theory.


