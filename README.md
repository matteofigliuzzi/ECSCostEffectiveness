# ECS Cost-effectiveness analyzer
Python library and dashboard to perform deterministic and probabilistic cost effectiveness analysis of
different carrier screening strategies.

## Mathematical Model

Model parameters:

- $p_{carrier}(d)$ carrier rate for disease $d$
- $p_{risk}(d)$ probability for the couple to be at risk for disease $d$
- $\eps_{CS}$ false negative rate for carrier screening
- $\rho$ intervention probability
- $\eps_{PGT}$ intervention failure probability

In case of recessive disease, the probability for a couple to be at risk is:

$$p_{risk}(d) = \left(p_{carrier}(d)\right)^2$$

In case of X-lined disease, the probability for a couple to be at risk is:

$$p_{risk}(d) = p_{carrier}(d)$$

Probability for a child to be affected in case strategy does not screen for disease $d$:

$$p_{affected}(d)=\frac{1}{4} p_{risk}(d)$$

Probability for a child to be affected in case strategy screens for disease $d$:

$$p_{affected}(d)=\frac{1}{4} p_{risk}(d)\left[ \eps_{CS} + (1-\eps_{CS})\rho + (1-\eps_{CS})(1-\rho)\eps_{PGT}  \right]$$

Intervention probability in case strategy screens for disease $d$:

$$p_{intervention}(d)=\frac{1}{4} p_{risk}(d) (1-\eps_{CS})(1-\rho)$$
$$

## Use docker to run ECS cost-effectiveness Dashboard locally 

Create docker image:

    docker build -t ecs_dashboard

Run the image as container:

    docker run -p 8080:8053 ecs_dashboard

Visit [0.0.0.0:8080](http://0.0.0.0:8080/) to access dashboard

Custom analysis can be uploaded uploading excel files with custom disease list and custom strategies.
The excel files should be organized as example files in data/ folder.

## Run cost-effectiveness analysis on jupyter notebook

A jupyter notebook to perform deterministic and probabilistic analysis is availalble in 
notebook/cost_effectivness_notebook.ipynb. Make sure that dependencies listed in requirements.txt are satisfied.





