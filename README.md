# Patterns of Persistence and Diffusibility across World's Languages 

## Resources
- OSF: https://osf.io/5sh62/?view_only=5d07119803c24743940a08777884cc33 
- According to  different set of languages in each graph, language contact params. are calculated anew each time.
   


## Data Structure
all the following data are stored in OSF page above.

```
- data
    |- colexifications
        |- colex_all_dedup.csv (all the colexification patterns in colexnet+)
        |- colex_freq_processed  (colexification frequencies extracted from Colexnet+)
    |- languages
        |- languages_all.csv (data collected from Glottolog, WALS, AUTOTYP, etc.)
        |- languages_colexnet.csv (1320 languages, the languages of colexnet+ which have geo information, 870,540 language pairs)
        |- languages_jaeger.csv (1558 languages, 1212903 language pairs )
        |- languages_colexnet_jaeger_inner.csv (912 languages, 250,369 language pairs, intersection)
        |- languages_colexnet_jaeger_outer.csv (1966 languages, 1931,595 language pairs, union)
    |- stage1
        |- word2colex (generated from stage1/wordlist2colex.py)
            |- abstract_words
            |- affective_loaded
            |- concrete_words
            |- emotion_semantics
            |- non-nuclear
            |- nuclear
            |- random
        |- language_contact_colexnet (language contact calculated based solely on colexnet)
        |- language_contact_colexnet_jaeger (language contact calculated based solely on intersection of colexnet and jaeger)
        |- language_contact_jaeger (language contact calculated based solely on jaeger)
        |- pmiLanguageDistance.csv (recently updated phonological pmi similarity between languages from Jäger (2018))
        |- lang2lang_coords.csv
        |- lang2lang_geodesic.csv
    |- stage2
        |- colex2cosine:
            |- cosine_distances (results from stage2/matrix2cosine.py)
            |- matrices         (results from stage2/colex2matrix.py)
                |- non-nuclear.csv (1334 langs, 10883 colex.)
                |- nuclear.csv (1334 langs, 9120 colex.)
                |- random.csv (1334 langs, 4064 colex.)
                |- emotion-semantics.csv  (1334 langs, 6150 colex.)
                |- abstract_words.csv (1334 langs, 66574 colex.)
                |- concrete_words.csv (1334 langs, 12267 colex.)
                |- affective_loaded.csv (1334 langs, 1965 colex.)
                |- aff_concrete_words.csv (1198 langs, 68 colex.)
                |- aff_concrete_words.csv (1333 langs, 866 colex.)
                
        |- controlled_colex2cosine # (control groups) evenly sample the colexifications 
            |- cosine_distances
            |- matrices
                |- nuclear.csv (langs 1334, colex.5000)
                |- non-nuclear.csv (langs 1334, colex. 5000)
                |- random.csv (langs 1334, colex. 4064)
                |- emotion_semantics.csv (langs 1334, colex. 5000)
                |- abstract_words.csv (langs 1334, colex. 10000)
                |- concrete_words.csv (langs 1334, colex. 10000)
                |- aff_abstract_words.csv (lang 1149, colex. 68)
                |- aff_concrete_words.csv (lang 1198, colex. 68)
        |- graphs (resulting graphs)
            |- colexnet
            |- jaeger
    |- stage3
        |- colexnet
        |- jaeger
        |- plots
        |- results
    |- stage4
        |- phon_colex_corr
        |- plots
        
            

```

## Code sources:
```
|- notebooks
    |- stage1_data_jaeger2022.ipynb (optional?, check)
    |- stage1_language_contact.ipynb 
    |- stage2_build_graphs.ipynb
    
|- src
    |- stage1
        |- wordlist2colex.py (get colexification patterns based ona wordlist)
        |- language_contact.py
    |- stage2
        |- colex2matrix.py (input: stage1/word2colex)
        |- generate_abs_affective_matrices.py
        |- matrix2cosine.py 
        |- generate_controlled_matrices.py (output: stage2/controlled_colex2cosine)
        |- build_language_graph.py 
    |- stage3
        |-g2df.py
        |-mixed_effects_analysis.py
        |- plot_colex_level1.py
        |- plot_colex_level2.py
        |- plot_colex_level3.py
        |- plot_phon_colex.py
    |- stage4
        |- display_colex_lang.py
        |- heatmap_plots.py
        |- phon_nuclear_correlation.py
        |- print_out_words.py
```


  
## Loading networkx graph

- to avoid security issues with pickle files, we store the graph nodes in json files and edges in txt files
  - graph directory: `data/stage2/graphs`
    - nodes (language iso3code) are stored as json files with language attributes
    - edges with their attributes are stored in txt file 

- code snippet to construct networkx graph

```
import networkx as nx
import json

edge_fh = open("data/stage2/graphs/colexnet/lang_graph.txt", "rb")
g = nx.read_edgelist(edge_fh)

nodes_fh = open("data/stage2/graphs/colexnet/lang_graph_nodes.json", "r")
g_nodes = json.load(nodes_fh)

# convert dictionary keys, values into list of tuples to be added to the graph
g_nodes_tuples = []
for lang, lang_attributes  in g_nodes.items():
    g_nodes_tuples.append((lang, lang_attributes))

g.add_nodes_from(g_nodes_tuples)
```

example node:
```
g.nodes["deu"]


output:
{'name': 'German',
 'family': 'Indo-European',
 'genus': 'Germanic',
 'parent': 'Global German',
 'branch': 'Global German',
 'glottocode': 'stan1295',
 'macroarea': 'Eurasia',
 'area': 'Europe',
 'timespan': [],
 'coord': [48.649, 12.4676]}

```

example edge:
```
g.edges["nld", "deu"]

output:

{'contact': 3,
 'geodist': 648.8953043040958,
 'neighbour': 1,
 'branch': 0,
 'area': 'Europe',
 'family': 'Indo-European',
 'genus': 'Germanic',
 'macroarea': 'Eurasia',
 'syntactic': 0.3474,
 'genetic': 0.39285000000000003,
 'emotion': 0.4684797556679733,
 'nuclear': 0.4531300650766711,
 'non-nuclear': 0.4924596901293124,
 'random': 0.3678957843672906,
 'concrete': 0.4024320673244818,
 'abstract': 0.4732505932023499,
 'aff_abstract': 0.9262289504160344,
 'phon': 0.3960052450492234}
```


# Building the rich Language Graph

## Stage 1

### 1. Generate colexification dataset per concept list


`python src/stage1/wordlist2colex.py $concepts$`
    
- `$concepts$`:
    - `nuclear` (core vocabulary)
    - `non-nuclear` (peripheral vocabulary)
    - `random` (randomly sampled 60 concepts which are not included in other vocabs)
    - `emotion_semantics` (emotion vocabulary investigated in Jackson et al. (2019))
    - `abstract_words` (highly abstract vocabulary)
    - `concrete_words` (highly concrete vocabulary)
  
[//]: # ()
[//]: # (## 2. Phonological pmi &#40;Jäger 2018&#41;)

[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;`notebooks/stage1_jaeger2022.ipynb`&#41;)
[//]: # ()
[//]: # ()
[//]: # (we used the latest compiled data &#40;2022&#41; from [Jäger2018].)

## 2. Geo information processing

`language_contact.py`

1. get the existant languages `lang2lang_coords.csv` #LANG_PAIRS: `6522896`
2. calculate geodesic distance of the coordinates `lang2lang_geodesic.csv`
3. create a graph from the geo information 
    - nodes: 2554, nodes: 3260181
    - node example:
        - `stand1295: {'name': 'German',
          'family': 'Indo-European',
          'parent': 'Global German',
          'branch': 'Global German',
          'iso3': 'deu',
          'area': 'Eurasia',
          'timespan': (),
          'coord': (48.649, 12.4676)} `
    - edge example:
        - `("stan1295", "dutc1256") ->
          {'contact': 13,
          'geodist': 648.8953043040958,
          'neighbour': 1,
          'branch': 0,
          'area': 1,
          'family': 1}`
        - contact: how many languages in between
        - geodist: geodesic distance in KM.
        - neighbour(binary): `1 (contact<=15) or 0`
        - branch: `1 (if two languages belong to the same language branch) , 0 (no), -1 (unknown)`
        - area: `1 (if two languages belong to the same language macroarea) , 0 (no), -1 (unknown)`
        - family: `1 (if two languages belong to the same language family) , 0 (no), -1 (unknown)`

__Model geo (dis)-similarity__:

- in-between contact languages
- geodesic distance in KM.
- neighbour or not (binary) `<-` based on contact languages.




[//]: # (````)

[//]: # ()
[//]: # (## 4. get lang2lang pmi from colexification patterns)

[//]: # ()
[//]: # (1. generate edgelists)

[//]: # (    - `python src/stage1/edgelists_colex_pmi.py data/stage1/glottocodes/ data/stage1/edgelists`)

[//]: # (2. generate pmi scores for language pairs)

[//]: # (    - `python src/stage1/colex_lang_pmi.py data/stage1/edgelists data/stage1/colex_pmi`````)

## 3. Language Branch calculation

Adjusted codes from [Gast, V. & Koptjevskaja-Tamm, M. (2022).].

`notebooks/stage1_get_language_branches.ipynb`

## 5. Ratings mapping 
`notebooks/stage1_ratings.ipynb`


# Stage 2 Build rich language graphs


## 1. get lang2lang similarity from bible frequency of shared colexification patterns

- colex freq from colexnet+ (bible): `data/colex_freq_processed`
- more statistics in the appendix of the paper.



### Genetic URIEL

- `genetic.csv` – A distance metric derived from the Glottolog hypothesized tree of language, representing the number of
  steps upward on the tree until the two languages are unified under a single node, divided by the number of branches in
  between L1 and the root. (In other words, the percentage of L1’s descent not shared by L2.) This has the advantage of
  correctly sorting languages by relation even in a tree with wildly different levels of detail between branches and
  families. The downside is that this relationship is not commutative, and the numbers do not have any absolute
  significance. (E.g., that L1 and L2 are related by “0.4” is not meaningful except in comparison with other relatives
  of L1;
  - get the average genetic distance (undirected)
  - `syntactic`.


## Build a rich language graph

`python src/stage2/build_language_graph.py $name$ $controlled$ $language_contact_folder$ $language_file$`

Examples:
- languages based on availability of languages in colexnet+:
`python src/stage2/build_language_graph.py colexnet $controlled$ data/stage1/languages_colexnet_contact data/languages/languages_colexnet.csv`

  - output:
    - edges and their attributes: `stage2/graphs/colexnet/{controlled_}language_graph.txt`
    - nodes and their attributes: `stage2/graphs/colexnet/{controlled_}language_graph_nodes.json`


- languages based on the availability in (Jaeger 2018): 
`python src/stage2/build_language_graph.py jaeger $controlled$ data/stage1/languages_colexnet_jaeger_outer data/languages/languages_colexnet_jaeger_outer.csv`

  - output:
     - edges and their attributes: `stage2/graphs/jaeger/{controlled_}language_graph.txt`
     - nodes and their attributes: `stage2/graphs/jaeger/{controlled_}language_graph_nodes.json`

# Stage 3 Experiment and Analysis


## 1. Convert language graphs to edgelists for further analysis:

[//]: # (- convert colex~phon graph)

[//]: # (  - `python src/stage3/g2df.py colexnet_phon`)

[//]: # (- convert colex graph )

[//]: # (  - `python src/stage3/g2df.py colexnet`)

- Convert graph to df
  
`python src/stage3/g2df.py data/stage2/graphs/colex_jaeger_outer/lang_graph.txt`


## 2.  [Mixed effects Regression Analysis](https://anonymous.4open.science/r/PersistenceAndDiffusibility-018F/README.md#mixed_effects_regression)

The mixed effects regression model we are using can be formulated as follows for readability:
1. For testing hypothesis of persistence of colexification patterns and phonological markups of languages:
   
`COLEX ~ PHYLO + ( 1 + CONTACT | RELATEDNESS)`

and

 `PHON ~ PHYLO + ( 1 + CONTACT | RELATEDNESS)`

The dependent variables are `COLEX` and `PHON`, accordingly, the independent variable is `PHYLO` (genetic distance). It is intended to test the fixed effects of `PHYLO` on the response `COLEX` or `PHON`, which are the coefficients we are estimating in the model. `RELATEDNESS` (the level of relatedness, e.g., lower-level, mid-level, higher-level, and unrelated) is the grouping variable for the random effects, and `CONTACT` (i.e., `GEO.Dist`, `Contact.Dist`, `Neighbour`) is the control variable that serves as a control in the random effects part of the model.

The more formal formulations are defined as follows:

`COLEX_{ij} = β_0 + β_{PHYLO} * PHYLO_{ij} + u_{0i} + (u_{CONTACT,0i} + u_{CONTACT,1i} * CONTACT_{ij}) + ε_{ij}`

and

`PHON_{ij} = β_0 + β_{PHYLO} * PHYLO_{ij} + u_{0i} + (u_{CONTACT,0i} + u_{CONTACT,1i} * CONTACT_{ij}) + ε_{ij}`

Where
* `COLEX_{ij}` and `PHON_{ij}` is the value of the dependent variable for observation `j` in group `i`, correspondingly;
* `β_0` is the fixed intercept;
* `PHYLO_{ij}` is the value of the variable `PHYLO` for observation `j` in group `i`.
* `u_{0i}` is the random intercept for group i (RELATEDNESS);
* `u_{CONTACT,0i}` is the random intercept for the variable `CONTACT` for group `i`;
* `u_{CONTACT,1i}` is the random slope for the variable `CONTACT` for group i;
* `CONTACT_{ij}`  is the value of the variable `CONTACT` for observation `j` in group `i`;
* `ε_{ij}` is the error term for observation `j` in group `i`.

2. For testing hypothesis of diffusibility of colexification patterns and phonological markups of languages:

	`COLEX ~ CONTACT + ( 1 + PHYLO | RELATEDNESS )`

	and

    `PHON  ~ CONTACT + (1 + PHYLO | RELATEDNESS )`
   
The dependent variables are `COLEX` and `PHON`, accordingly, the independent variable is `CONTACT` (i.e., `GEO.Dist`, `Contact.Dist`, `Neighbour`). It is intended to test the fixed effects of `CONTACT` on the response `COLEX` or `PHON`, which are the coefficients we are estimating in the model. `RELATEDNESS` (the level of relatedness, e.g., family, branch, or macroarea) is the grouping variable for the random effects, and  `PHYLO` (genetic distance) is the control variable that serves as a control in the random effects part of the model.

The more formal formulations are defined as follows:

`COLEX_{ij} = β_0 + β_{CONTACT} * CONTACT_{ij} + u_{0i} + (u_{PHYLO,0i} + u_{PHYLO,1i} * PHYLO_{ij}) + ε_{ij}`

and

`PHON_{ij} = β_0 + β_{CONTACT} * CONTACT_{ij} + u_{0i} + (u_{PHYLO,0i} + u_{PHYLO,1i} * PHYLO_{ij}) + ε_{ij}`

Where
* `COLEX_{ij}` and `PHON_{ij}` is the value of the dependent variable for observation `j` in group `i`, correspondingly;
* `β_0` is the fixed intercept;
* `CONTACT_{ij}` is the value of the variable `CONTACT` for observation `j` in group `i`.
* `u_{0i}` is the random intercept for group `i` (`RELATEDNESS`);
* `u_{PHYLO,0i}` is the random intercept for the variable `PHYLO` for group `i`;
* `u_{PHYLO,1i}` is the random slope for the variable `PHYLO` for group `i`;
* `PHYLO_{ij}`  is the value of the variable `PHYLO` for observation `j` in group `i`;
* `ε_{ij}` is the error term for observation `j` in group `i`.


#### Run scripts:

- colexnet 
  - `python src/stage3/mixed_effects_analysis.py $result_file$ colexnet`

- phon
  - `python src/stage3/mixed_effects_analysis.py $result_file$ phon`


## 3. Plot
- phon
  - `python src/stage3/plot_phon_colex.py $result_file$ `

- colex
  - three levels of colex. plots for presenting differential persistence and diffusibility of lexicon sets.

