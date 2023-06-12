# Patterns of Persistence and Diffusibility for 1561 Languages: In the case of crosslingual colexifications


- control group: random lexica
- consulting highly familiar lexicon?
  - familiarity and colexifications.
    - only found english ones....
    


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


## 2. Phonological pmi (Jäger 2018)

`notebooks/stage1_jaeger2022`

we used the latest compiled data (2022) from [Jäger2018].


## 3. Geo information

`notebooks/language_contact.ipynb`

- using `Glottocode`
- `data/stage1/pmiLanguageDistane.csv` union `data/colexifications/colex_all_dedup.csv` -> `languages_coords.csv` get the languages where there are geo coordinates.
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



# Stage 2 Analysis
## 1. generate graphs:

`python src/stage2/build_graphs.py`
### Graphs Data
- `colex_geo`
- `phon_colex_geo`
- `phon_geo` 




# Stage 3 Plots.


