# Code-Transformation-Transformer

The official implementation for the paper:
* __Understanding the Robustness of Transformer-Based Code Intelligence via Code Transformation: Challenges and Opportunities__

This paper has been accepted by **IEEE Transactions on Software Engineering (TSE)**.

*   **Published Version (Recommended):** [[IEEE Xplore](https://ieeexplore.ieee.org/document/10843180/)]
*   *Initial Preprint (Archival):* [[arXiv](https://arxiv.org/abs/2207.04285)]

**Please note:** The version published in TSE is the definitive and significantly improved version. It incorporates substantial enhancements, deeper analysis, and more detailed discussions resulting from the peer review process (major and minor revisions) compared to the initial arXiv preprint, which had limitations and shallower discussions.


The repository uses [CodeSearchNet Dataset](https://github.com/github/CodeSearchNet) with Java and Python languages.

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
@article{li2025understanding,
  title={Understanding the Robustness of Transformer-Based Code Intelligence via Code Transformation: Challenges and Opportunities},
  author={Li, Yaoxian and Qi, Shiyi and Gao, Cuiyun and Peng, Yun and Lo, David and Lyu, Michael R and Xu, Zenglin},
  journal={IEEE Transactions on Software Engineering},
  year={2025},
  publisher={IEEE}
}
```

