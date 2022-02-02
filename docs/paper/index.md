(yowt)=
# Parameter identification of Vessel Manoeuvring Models

```{admonition} Authors
:class: tip
**Martin Alexandersson**, **Wengang Mao** & **Jonas W. Ringsberg**

[Martin Alexandersson](mailto:maralex@chalmers.se),

Department of Mechanics and Maritime Sciences,  
Chalmers University of Technology,  
Gothenburg, Sweden
```

(abstract)=
## Abstract ##
> The manoeuvring performance of ships can be assessed in many ways, where model test with a free moving model is the most established and accurate method to confirm the compliance with the IMO standards. Going beyond the results from a model test campaign, looking at alternative scenarios with other speeds or entirely other manoeuvres or even bridge simulations, a prediction model is needed. The prediction model is trained with supervised learning on some data where the expected output of the model is known. The model can then be used to predict new data when investigating alternative manoeuvring scenarios. For manoeuvring the prediction model is usually a simulation with a Vessel Manoeuvring Model (VMM). A method to train this kind of models using motion regression is used in this paper. The training is conducted with several VMM:s on a model tests series for one vessel to propose the best prediction model. The methodology is aimed to be usable for other cases as well, where replacing the model tests data with full scale data from real ship is the goal for the future.   

## Static Document ##

In addition to this online document, the paper can be downloaded as a PDF
either from [OpenReview] or [arXiv].
The source of this article is available on [GitHub][source].

<a class="btn btn-outline-primary"
   href="https://openreview.net/forum?id=i4zpuNRiU4G">{fa}`file-pdf,style=fas` OpenReview (PDF)</a>
<a class="btn btn-outline-primary"
   href="https://arxiv.org/abs/2107.06639">{fa}`file-pdf,style=fas` arXiv (PDF)</a>
<a class="btn btn-outline-primary"
   href="https://github.com/so-cool/you-only-write-thrice">{fa}`book,style=fas` GitHub (Jupyter Book)</a>

## Review ##

This paper has been reviewed on [OpenReview].

<a class="btn btn-outline-success"
   href="https://openreview.net/forum?id=i4zpuNRiU4G">{fa}`vote-yea,style=fas` OpenReview</a>


## Citation ##

```BibTeX
@inproceedings{sokol2021you,
  title     = {{Y}ou {O}nly {W}rite {T}hrice:
               {C}reating {D}ocuments, {C}omputational {N}otebooks and
               {P}resentations {F}rom a {S}ingle {S}ource},
  author    = {Sokol, Kacper and Flach, Peter},
  booktitle = {{B}eyond static papers:
               {R}ethinking how we share scientific understanding in {ML} --
               {ICLR} 2021 workshop},
  year      = {2021},
  note      = {arXiv preprint arXiv:2107.06639},
  doi       = {10.5281/zenodo.5106062}
}
```

