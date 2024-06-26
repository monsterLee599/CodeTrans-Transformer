# Code-Transformation-Transformer

The official implementation of:
* __A Closer Look into Transformer-Based Code Intelligence Through Code Transformation: Challenges and Opportunities__ [[arxiv](https://arxiv.org/abs/2207.04285)] 

The repository use [CodeSearchNet Dataset](https://github.com/github/CodeSearchNet) with Java and Python languages.

## Repository structure
* `codetrans`: code transformation strategies in our paper.
* `dataset`: scripts for processing CodeSearchNet datasets.
* `CSM`: code for code summarization (CSM) task (additional preprocessing, models, training etc)
* `CC`: code for Code Completion (CC) task (additional preprocessing, models, training etc)
* `CS`: code for Code Search (CS) task (additional preprocessing, models, training etc)

__See README in each directory for details.__

## Run

The code was tested on a system with Ubuntu 18.04. Experiments were run using a Tesla V100 GPU. Required libraries are listed in `requirments.txt` in different tasks directories. The implementation is based on PyTorch>=1.5 and Tensorflow>=2.2.

Running experiments:
1. Download data, see `datasets` for details;
2. Preprocess data for a task you are interested in, see `CS`, `CSM` or `CC` for details;
3. Run the experiment you are interested in.

## Attribution

Parts of this code are based on the following repositories:

* [Empirical Study of Transformers for Source Code](https://github.com/bayesgroup/code_transformers) 
* [A Transformer-based Approach for Source Code Summarization](https://github.com/wasiahmad/NeuralCodeSum) 
* [Code Completion by Feeding Trees to Transformers](https://github.com/facebookresearch/code-prediction-transformer)
* [Semantic Code Search](https://github.com/AuthEceSoftEng/CodeTransformer)
* [CodeBert](https://github.com/microsoft/CodeBERT/tree/master)
* [CodeXGLUE](https://github.com/microsoft/CodeXGLUE)

## Citation

If you found this code useful, please cite our paper
```
@article{li2022closer,
  title={A closer look into transformer-based code intelligence through code transformation: Challenges and opportunities},
  author={Li, Yaoxian and Qi, Shiyi and Gao, Cuiyun and Peng, Yun and Lo, David and Xu, Zenglin and Lyu, Michael R},
  journal={arXiv preprint arXiv:2207.04285},
  year={2022}
}
```

