**AST** stands for **Abstract Syntax Tree**.

## What is an Abstract Syntax Tree?

An **Abstract Syntax Tree (AST)** is a tree representation of the abstract syntactic structure of source code. Each node
of the tree denotes a construct occurring in the programming language.

### Key Characteristics:

1. **Abstract** - It abstracts away syntactic details like whitespace, brackets, and semicolons
2. **Syntax** - It represents the grammatical structure of the code
3. **Tree** - It's organized as a hierarchical tree structure

### Example:

For the Python code:

```python
x = 5 + 3 * 2
```

The AST would look like:

```
Assign
├── targets: [Name(id='x')]
└── value: BinOp
    ├── left: Constant(value=5)
    ├── op: Add()
    └── right: BinOp
        ├── left: Constant(value=3)
        ├── op: Mult()
        └── right: Constant(value=2)
```

### Why ASTs are Important in Security Linting:

1. **Structural Analysis** - Can analyze code structure regardless of formatting
2. **Pattern Matching** - Can detect dangerous patterns like SQL injection
3. **Context Awareness** - Understands the relationship between code elements
4. **Language Agnostic** - Same concepts apply across programming languages

### In Python's `ast` Module:

```python
import ast

code = "x = 5 + 3"
tree = ast.parse(code)
print(ast.dump(tree, indent=2))
```

This is why the security linter uses `ast.NodeVisitor` - it traverses the AST to analyze code structure and identify
security vulnerabilities programmatically, rather than just searching for text patterns.