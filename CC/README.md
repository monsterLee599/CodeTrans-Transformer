
# Code Completion Task

## Dependencies

To install all dependencies, you can optionally run the following command:
```sh
pip install -r requirements.txt
```

## Running Experiments

Our implementation is based on [this repository](https://github.com/bayesgroup/code_transformers/tree/main/cc).

The file `cc_all_data.xlsx` contains the results of our code transformation.

Here is a brief description of the models used in our experiments:

- **text_pos**: A sequence-based Transformer with absolute position encoding.
- **text_rel**: A sequence-based Transformer with relative position encoding.
- **ast_pos**: An AST-based Transformer with absolute position encoding.
- **ast_rel**: An AST-based Transformer with relative position encoding.
