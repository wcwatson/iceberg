# Estimating Population Size via Musicological "Icebergs"

This repo contains the source code for Iceberg, a Python library that implements two methods for estimating the true size of a population given a collection of samples taken without replacement.
For more details on how icebergs can be musicological, and what such objects have to do with estimating population size, see [Michael Scott Cuthbert, "Tipping the Iceberg: Missing Italian Polyphony from the Age of Schism," Musica Disciplina 54 (2009): 39–74](https://www.jstor.org/stable/25750547?seq=1).

## Installation & Use

You can install Iceberg from the command line, just like any other Python library.
```shell
$ pip install iceberg-est
```

Once installed, you can use the functionality by importing the relevant modules.
```python
import iceberg.estimate as est
import iceberg.simulate as sim
```

## Contents

* `iceberg` contains the Python library, including two modules
  * `iceberg.estimate` exposes functions that implement the estimation algorithms
  * `iceberg.simulate` exposes functions that simulate situations illustrating the functionality of the estimation algorithms
* `docs` contains descriptions of the estimation algorithms, examples of their use, and comparisons of their effectiveness
