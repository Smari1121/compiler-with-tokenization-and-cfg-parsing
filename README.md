# Compiler Frontend: Tokenization and Syntactic Validation

This repository contains a Python implementation of a simple compiler
frontend that performs **lexical analysis (tokenization)** and
**syntactic validation** for a toy programming language.

The implementation is intentionally explicit and lightweight, focusing
on correctness and clarity rather than completeness or optimization.

---

## Overview

The compiler frontend works in two stages:

1. **Tokenization (Lexical Analysis)**  
2. **Grammar Checking (Syntactic Analysis)**  

For each line of input source code, the program reports whether the line
contains:
- **No Error**
- **Lexical Error**
- **Syntax Error**

The output for all input lines is written to a corresponding output
file.

---

## Lexical Analysis (Tokenizer)

The tokenizer processes the source code character by character and
classifies lexemes into tokens.

### Token Types
- `KEYWORD` — reserved words (`if`, `else`, `print`)
- `IDENTIFIER` — valid identifiers (letters or `_` followed by letters,
  digits, or `_`)
- `INTEGER` — integer literals
- `FLOAT` — floating-point literals
- `SYMBOL` — operators and punctuation

### Token Hierarchy
If a lexeme matches both an identifier pattern and a keyword, it is
classified as a **keyword**.  
For example, `if` is recognized as a keyword, not an identifier.

### Lexical Errors
Lexical errors are raised for invalid tokens, such as:
- identifiers starting with digits (e.g., `2xi`)
- malformed numeric literals

---

## Syntactic Analysis

After tokenization, the token stream is validated using a **recursive
descent parser**.

The parser checks whether the token sequence conforms to a simplified
statement grammar supporting:
- conditional statements (`if` / `else`)
- expressions with arithmetic and comparison operators
- simple statements consisting of identifiers, numbers, or keywords

The grammar is implemented procedurally rather than using a parser
generator, to make the parsing logic explicit and easy to follow.

### Syntax Errors
Syntax errors are reported when:
- tokens appear in invalid positions
- keywords such as `else` appear without a corresponding `if`
- expressions or statements violate the expected structure

---

## Input and Output Behavior

### Input
- The program takes a **file path** as a command-line argument.
- Each line in the input file is treated as an independent statement.

### Output
- For each input line, the program outputs one of:
  - `No Error`
  - `Lexical Error`
  - `Syntax Error`
- The results are written to an output file named:
<input_filename>_output.txt
