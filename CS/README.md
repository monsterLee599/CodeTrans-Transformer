# Code Search Task

## Dependencies

This task is based on TensorFlow, so you should create a new environment to execute the code.

To install all dependencies, you can run the following command:

```sh
pip install -r requirements.txt
```

## Running Experiments

Our implementation is based on:

- [Semantic Code Search](https://github.com/AuthEceSoftEng/CodeTransformer)





## Results

The file `cs_all_data.xlsx` contains the results of our code transformation.

## Models Used

Here is a brief description of the models used in our experiments:

- **text_pos**: A sequence-based Transformer with absolute position encoding.
- **text_rel**: A sequence-based Transformer with relative position encoding.
- **ast_pos**: An AST-based Transformer with absolute position encoding.
- **ast_rel**: An AST-based Transformer with relative position encoding.

