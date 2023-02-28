import spacy
import streamlit as st
import spacy_streamlit as sst
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacyfishing

st.set_page_config(layout='wide')
col1, col2, col3= st.columns(3)
nlp=spacy.load(r'./model-nel')



with col1: 
    text = st.text_area('**sett in tekst her:**', value='''Det solfylte sommerbildet med brudefølget i båtene, stavkirken på odden og vestlands- naturen med fjord og fjell er et typisk uttrykk for nasjonalromantikkens opplevelse av norsk natur og folkeliv. Kunstnerne spilte en vesentlig rolle når det gjaldt å definere en nasjonal egenart etter at Norge hadde fått sin grunnlov i 1814. Dette motivet, som så sterkt uttrykker 1800-tallets skjønnhetsidealer, har vært dyrket som et ”ikon” av generasjoner av nordmenn. Maleriet har vært overført til teaterscenen både som levende tablå og ballett, og motivet er blitt ledsaget av dikt og musikk.

                        #Gjennom grafiske reproduksjoner fikk Brudeferd i Hardanger stor utbredelse, og på grunn av motivets spesielle popularitet har kunstnerne utført maleriet i flere versjoner. Adolph Tidemand var den første norske kunstner som slo seg ned i Düsseldorf. Sin ambisjon om å bli historiemaler oppga han for å bli folkelivsskildrer. Men Tidemand gir en ny verdighet til bøndene, og dikteren Bjørnstjerne Bjørnson skal ha sagt at uten Tidemands malerier hadde han ikke kunnet skrive sine bondefortellinger.

                        #Landskapsmaler Hans Gude, som var drøye ti år yngre enn Tidemand, presenterer her som 23-åring en storslagen skildring av norsk natur. Selv om det ikke dreier seg om en direkte gjengivelse av et bestemt landskap, er komposisjonen satt sammen av nøyaktige naturobservasjoner fra forskjellige steder i hjemlandet. Tidemand og Gude har utført flere malerier sammen, der alle motivene viser folk som er ute i båt.''', max_chars=1000000)
    if st.button("analyser tekst!"):
        st.write("analyserer tekst...")
        doc=nlp(text)
        st.write("ferdig!")

with col2:

    st.write('**Her er ting og tang vi har funnet i teksten**')
    st.write('*Hvis vi har funnet koblinger til kulturNAV eller Wikidata, kan du trykke på entitetsnavnet for å komme til den aktuelle posten*')
    
    for ent in doc.ents:
        if ent.ent_id_!="" and ent.kb_id_!="":
            st.markdown(f"[{ent.text}](https://kulturnav.org/{ent.ent_id_}) - [wikidata](https://www.wikidata.org/entity/{ent.kb_id_})")
            #print(ent.text, ent.id_)
        elif ent.kb_id_!="":
            st.markdown(f"[{ent.text}](https://www.wikidata.org/entity/{ent.kb_id_})")
            #print(ent.text, ent.kb_id_)
        else:
            st.write(ent.text, ent.label_)

with col3: 
    sst.visualize_ner(doc, labels=nlp.get_pipe("ner").labels, key='s1', show_table=False, title="")
