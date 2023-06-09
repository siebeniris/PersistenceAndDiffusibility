# PersistenceAndDiffusibility

Patterns Persistence and Diffusibility across Languages: In the case of crosslingual colexifications

# colexifications

- wn 0.1
- colexnet+

- `data/colexifications`
    - clics3.csv
    - colex_wn_phon.csv
    - colexnet.csv


# persistence

- stability?
    - schutze's definition using concreteness.

- diffusibility
    - language contact.
    - wikipron
        - see the intersection of wikipron with both colexification networks.



# Stage 1

## 1. Generate colexification dataset per wordlist 

`python src/stage1/core_vocab_colex.py nuclear data/stage1/colex_wn_emotion.csv`

`Glottocode`
####  nuclear

- wn, len 1980472, len 17386, len 9313 langs 108
- clics3, len 76202, len 8154 .len 6852 langs 1129
- colexnet, len 12288641,len 451798,len 185244 langs 1329
- all, len 14217010, len 473388, len 200965, langs 2172

### peripheral

- wn, len 1980472,len 29532,len 15466 langs 114
- clics3, len 76202, len 4703,len 13103 langs 1468
- colexnet, len 12288641, len 603707, len 238447 langs 1329
- all, len 14217010, len 639764, len 266220, langs 2475


### emotion semantics

- wn, len 1980472, len 10867, len 5548 langs 63
- clics3, len 76202, len 1107, len 688 langs 205
- colexnet, len 12288641, len 337278, len 135047, langs 1329
- all, len 14217010, len 347199, len 141072, langs 1451


## 2. phonological pmi (Jaeger 2018)

`notebooks/stage1_jaeger2022`

we used the latest compiled data (2022) from [Jaeger2018].


## 3. get geo information

`notebooks/language_contact.ipynb`

- using `Glottocode`
- `data/stage1/pmiLanguageDistane.csv` -> `languages_coords.csv` get the languages where there are geo coordinates.
  #LANGUAGES **1561**

1. get the existant languages `lang2lang_coords.csv`
2. calculate geodesic distance of the coordinates `lang2lang_geodesic.csv`
3. create a graph from the geo information `language_geo_graph.pickle`
    - nodes: 1561, nodes: 1217580
    - node example: `"pawa1225" -> {'coord': (-6.88021, 145.081)} `
    - edge example: `('pawa1255','guin1254') -> {'contact': 1242, 'geodist': 17172.307067554568}`
        - contact: how many languages in between
        - geodist: geodesic distance in KM.


__Model geo (dis)-similarity__:
- in-between contact languages
- geodesic distance in KM.
- neighbour or not (binary) <- based on contact languages.


## 4. get lang2lang pmi from colexification patterns
1. generate edgelists 
    - `python src/stage1/edgelists_colex_pmi.py data/stage1/glottocodes/ data/stage1/edgelists`
2. generate pmi scores for language pairs 
   - `python src/stage1/colex_lang_pmi.py data/stage1/edgelists data/stage1/colex_pmi`




