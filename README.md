# Patterns of Persistence and Diffusibility across World's Languages 

# Graphs
- Zenodo: [https://zenodo.org/record/8074593](https://zenodo.org/record/8074593)
- According to  different set of languages in each graph, language contact params. are calculated anew each time.

# Lexicons

- concreteness 
  - abstract words
  - concrete words
- affectiveness
  - extreme
- nuclear
- peripheral
- emotion semantics



[//]: # (# Colexifications)

[//]: # (- frequency of the colexifications in COLEXNET+)

[//]: # (  - input:)

[//]: # (    - `colexifications/colexnet+.csv`)

[//]: # (    - `ColexificationNet/output/ngrams/updated`)

[//]: # (  - output: `freq_graph.pickle`)

[//]: # (  - script `CrossCoLEX/src/preprocessing/data/get_colex_freq.py`)



# Stage 1




## 1. Generate colexification dataset per wordlist


`python src/stage1/wordlist2colex.py nuclear`

`Glottocode`

[//]: # ()
[//]: # (#### nuclear)

[//]: # ()
[//]: # (- wn, len 1980472,)

[//]: # (  len 17386,)

[//]: # (  len 9313, langs 108)

[//]: # (- clics3, len 76202,)

[//]: # (  len 8154,)

[//]: # (  len 6852, langs 1129)

[//]: # (- colexnet, len 12286130,)

[//]: # (  len 451711,)

[//]: # (  len 185208,langs 1329)

[//]: # (- all, len 14214499, len 473301, len 200929, langs 2172)

[//]: # ()
[//]: # (### peripheral)

[//]: # ()
[//]: # (- wn, len 1980472)

[//]: # (  len 29532)

[//]: # (  len 15466 langs 114)

[//]: # (- clics3, len 76202)

[//]: # (  len 14703)

[//]: # (  len 13103 langs 1468)

[//]: # (- colexnet, len 12286130)

[//]: # (  len 603667)

[//]: # (  len 238430 langs 1329)

[//]: # ()
[//]: # (- all, len 14214499 ,len 639724 , len 266203, langs 2475)

[//]: # ()
[//]: # (### emotion semantics)

[//]: # ()
[//]: # (- wn, len 1980472 ,len 10867 , len 5548 langs 63)

[//]: # (- clics3, len 76202 ,len 1107 , len 688 langs 205)

[//]: # (- colexnet, len 12286130 ,len 337268 ,len 135042 langs 1329)

[//]: # (- all, len 14214499 , len 347189 , len 141067,langs 1451)



## 2. Phonological pmi (Jäger 2018)

`notebooks/stage1_jaeger2022`

we used the latest compiled data (2022) from [Jäger2018].

## 3. Geo information

`notebooks/language_contact.ipynb`

- using `Glottocode`
- `data/stage1/pmiLanguageDistane.csv` union `data/colexifications/colex_all_dedup.csv` -> `languages_coords.csv` get
  the languages where there are geo coordinates.
  #LANGUAGES `2554`
    - phon: 1563
    - colex: 2933
    - union: 2933
    - intersected with geo info: 2554


1. get the existant languages `lang2lang_coords.csv` #LANG_PAIRS: `6522896`
2. calculate geodesic distance of the coordinates `lang2lang_geodesic.csv`
3. create a graph from the geo information `language_geo_graph.pickle`
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






## 4. get lang2lang pmi from colexification patterns

1. generate edgelists
    - `python src/stage1/edgelists_colex_pmi.py data/stage1/glottocodes/ data/stage1/edgelists`
2. generate pmi scores for language pairs
    - `python src/stage1/colex_lang_pmi.py data/stage1/edgelists data/stage1/colex_pmi`

## 5. Language Branch calculation

Adjusted codes from [Gast, V. & Koptjevskaja-Tamm, M. (2022).].

`notebooks/stage1_get_language_branches.ipynb`

## 6. Ratings mapping 
`notebooks/stage1_ratings.ipynb`


# Stage 2 Build graphs




## 1. get lang2lang similarity from bible frequency of shared colexification patterns

- colex freq from colexnet+ (bible): `/Users/yiyichen/Documents/experiments/CrossCoLEX/data/graphs/freq_graph.pickle`
- `["aaron":"drink"]:{'lang': {'nij'}, 'realizations': {'nij': {'harun'}}, 'frequency': {'nij': 21}}`

- `python src/stage2/colex2cosine.py [xx wordlist]`

- `notebooks/stage2_colexnet.ipynb`


- abstract words
  - non-na values:  1240073
  - remaining langs 1327 and colex 65771, 
- concrete words:
  - non-na values:  352774
  - remaining langs 1327 and colex 12132, language pairs: 879801
- affective extreme:
  - non-na values:  43446
  - remaining langs 1325 and colex 1948, language pairs: 877150


# Stage 3 Analysis

## 1. generate graphs:

- COLEXNET:
` python src/stage2/language_contacts_graphs.py colexnet data/stage1/language_contact_colexnet data/languages/languages_colexnet.csv data/stage2/graphs`
    - `stage2/graphs/colexnet_geo_graph.pickle`   langs 1320 - lang pairs 870540

- PHON:
`python src/stage2/language_contacts_graphs.py phon data/stage1/language_contact_jaeger data/languages/languages_jaeger.csv data/stage2/graphs `
  - `stage2/graphs/phon_geo_graph.pickle`, langs 1558 - lang pairs 1212903
- COLEXNET_PHON: 
`python src/stage2/language_contacts_graphs.py colexnet_phon data/stage1/language_contact_colexnet_jaeger data/languages/languages_colexnet_jaeger.csv data/stage2/graphs`
  - `stage2/graphs/colexnet_phon_geo_graph.pickle`

  

### Genetic URIEL

- `genetic.csv` – A distance metric derived from the Glottolog hypothesized tree of language, representing the number of
  steps upward on the tree until the two languages are unified under a single node, divided by the number of branches in
  between L1 and the root. (In other words, the percentage of L1’s descent not shared by L2.) This has the advantage of
  correctly sorting languages by relation even in a tree with wildly different levels of detail between branches and
  families. The downside is that this relationship is not commutative, and the numbers do not have any absolute
  significance. (E.g., that L1 and L2 are related by “0.4” is not meaningful except in comparison with other relatives
  of L1;
  - get the average genetic distance (undirected)
  - syntactic.

## 2. convert graph to edgelists for further analysis:

- convert colex~phon graph
  - `python src/stage3/g2df.py colexnet_phon`
- convert colex graph 
  - `python src/stage3/g2df.py colexnet`


## 3. Mixed effects Regression Analysis
- colexnet 
  - `python src/stage3/mixed_effects_analysis.py data/stage3/controlled_colexnet_geo_graph_edges.csv colexnet`

- phon.
  - `python src/stage3/mixed_effects_analysis.py data/stage3/colexnet_phon_geo_graph_edges.csv phon`
  - 
## 4. Plot
- phon
  - `python src/stage3/plot_phon_colex.py data/stage3/results/all/phon_reports_mixed_effects2.csv `

- colex
  - three levels of colex. plots

