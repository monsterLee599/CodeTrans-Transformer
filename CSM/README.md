Here's the enhanced README in Markdown format:

# Code Summarization Task

## Dependencies

To install all dependencies, you can run the following command:
```sh
pip install -r requirements.txt
```

## Running Experiments

Our implementation is based on:

- [Empirical Study of Transformers for Source Code](https://github.com/bayesgroup/code_transformers/tree/main/vm_fn)
- [A Transformer-based Approach for Source Code Summarization (NeuralCodeSum)](https://github.com/wasiahmad/NeuralCodeSum)

**Note:** The Empirical Study is designed for the function rename prediction task, so the target objective is different from code summarization. We use the data processing scripts from the Empirical Study.

NeuralCodeSum uses sub-tokenization for effective code summarization. In our default experiments, we did not split the sub-tokens.

## Results

The file `csm_all_data.xlsx` contains the results of our code transformation.

## Models Used

Here is a brief description of the models used in our experiments:

- **text_pos**: A sequence-based Transformer with absolute position encoding.
- **text_rel**: A sequence-based Transformer with relative position encoding.
- **ast_pos**: An AST-based Transformer with absolute position encoding.
- **ast_rel**: An AST-based Transformer with relative position encoding.

