# ECS Cost-effectiveness analyzer
Python library and dashboard to perform deterministic and probabilistic cost effectiveness analysis of
different carrier screening strategies.


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

## Mathematical Model
<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
  type="text/javascript">
</script>

This sentence uses `$` delimiters to show math inline:  $\sqrt{3x-1}+(1+x)^2$

This is an inline equation: $$V_{sphere} = \frac{4}{3}\pi r^3$$,<br>
followed by a display style equation:

$$V_{sphere} = \frac{4}{3}\pi r^3$$


    '''$\mathcal{a}$'''