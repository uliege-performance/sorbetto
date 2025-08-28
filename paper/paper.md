---
title: 'Sorbetto: A Python Package for Producing Classification Tiles With Different Flavors'
tags:
  - Python
  - performance
  - classification
  - Tiles
authors:
  - name: Sébastien Piérard
    orcid: 0000-0001-8076-1157
    affiliation: 1
    corresponding: true
  - name: Anaïs Halin
    orcid: 0000-0003-3743-2969
    affiliation: 1
  - name: François Marelli
    orcid: 0000-0002-8261-238X
    affiliation: 2
  - name: Simon Pernas
    affiliation: 3
  - name: Jérôme Pierre
    orcid: 0009-0006-3933-2995
    affiliation: 1
affiliations:
 - name: University of Liège (ULiège), Belgium
   index: 1
 - name: University of Mons (UMons), Belgium
   index: 2
 - name: Multitel, Belgium 
   index: 3
date: 5 September 2025
bibliography: paper.bib
---

# Summary

This is the summary. 

# Statement of need

`sorbetto` is a Python package for producing classification tiles with different flavors. 

`sorbetto` was designed to be used by machine learning researchers. It has already been
used in a number of scientific publications [@Pearson:2017]. 

# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from...

# References