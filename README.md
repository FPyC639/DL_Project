# Deep Learning DS 677-003 Class Project
## New Jersey Institute of Technology

# Generating Responses from Code using StarCoder Large Language Model

Avina Akarmi, Jose M Serra Jr

## I. Introduction

Using a Large Language Model for the target language of C++ we generated responses from code through an iterative process as shown in the BigCoder Project. This process involves using prompts to the Large Language Model The first epoch of work consisted of downloading the code that is going to be used in this process. The first Python script that was used allowed us to scrape a sample from HuggingFace Repo where the pointers to the S3 Bucket for the code, and then after downloading the data it was used to ensure validated that the data had top-level functions. This sets up the project to then follow a pipeline for users to be able generate instructions from coding snippets, and responses from instructions. This is done through a series of Linux scripts that then execute the Python script with the various parameters. This method allows modularity for the variations of the languages that can be continued being done.


## II. Dataset

 The dataset consisted of C++ code gathered through the BigCode Project. Our main task was to filter for code that did not have any pending tasks for an individual to do as well as being a top-level function. A top-level function is a function that is not nested in another function as well as not part of a class definition in the object-oriented programming paradigm. 

# Future Work

- Rust
- Java


## Acknowledgements

 - Professors at NJIT
 - Teaching Assistants at NJIT


## Authors

- [@avinanakarmi](https://github.com/avinanakarmi)
- [@FPyC639](https://github.com/FPyC639)
