import spacy
import streamlit as st
import spacy_streamlit as sst
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(layout='wide')
col1, col2, col3= st.columns(3)

nlp=spacy.load(r'./nlp_combine')

def concordance(doc, size):
    conc=[]
    for ent in doc.ents:
        try:
            indexb=ent.start_char - size
        except: 
            indexb=0
        try:
            indexe=ent.end_char + size
        except: 
            indexe=len(doc.text)
        conc.append([ent.label_, ent, doc.text[(indexb):(indexe)]])
    return conc

with col1: 
    text = st.text_area('**sett in tekst her:**', value='''Det solfylte sommerbildet med brudefølget i båtene, stavkirken på odden og vestlands- naturen med fjord og fjell er et typisk uttrykk for nasjonalromantikkens opplevelse av norsk natur og folkeliv. Kunstnerne spilte en vesentlig rolle når det gjaldt å definere en nasjonal egenart etter at Norge hadde fått sin grunnlov i 1814. Dette motivet, som så sterkt uttrykker 1800-tallets skjønnhetsidealer, har vært dyrket som et ”ikon” av generasjoner av nordmenn. Maleriet har vært overført til teaterscenen både som levende tablå og ballett, og motivet er blitt ledsaget av dikt og musikk.

                        #Gjennom grafiske reproduksjoner fikk Brudeferd i Hardanger stor utbredelse, og på grunn av motivets spesielle popularitet har kunstnerne utført maleriet i flere versjoner. Adolph Tidemand var den første norske kunstner som slo seg ned i Düsseldorf. Sin ambisjon om å bli historiemaler oppga han for å bli folkelivsskildrer. Men Tidemand gir en ny verdighet til bøndene, og dikteren Bjørnstjerne Bjørnson skal ha sagt at uten Tidemands malerier hadde han ikke kunnet skrive sine bondefortellinger.

                        #Landskapsmaler Hans Gude, som var drøye ti år yngre enn Tidemand, presenterer her som 23-åring en storslagen skildring av norsk natur. Selv om det ikke dreier seg om en direkte gjengivelse av et bestemt landskap, er komposisjonen satt sammen av nøyaktige naturobservasjoner fra forskjellige steder i hjemlandet. Tidemand og Gude har utført flere malerier sammen, der alle motivene viser folk som er ute i båt.''', max_chars=1000000)
    doc=nlp(text)

    cc=concordance(doc, 50)
    df=pd.DataFrame(cc, columns=['Label', 'Entity', 'Context']).sort_values('Label')
    df = df.astype(str)
    df=df.style
    st.write('**Entiteter i kontekst med labels**')      
    st.dataframe(df, use_container_width=True)

with col2:

    st.write('**Hele teksten med labels**')
    sst.visualize_ner(doc, labels=nlp.get_pipe("ner").labels, key='s1', show_table=False, title="")

with col3: 
    st.write('''**Ordsky for teksten**''') 
    labels=st.multiselect('Select labels for wordcloud:', options=nlp.pipe_labels['ner'],  default=nlp.pipe_labels['ner'])
    nouns=[]
    #print(nlp2.pipe_names)
    for tok in doc:
        dep=tok.is_stop
        #print(tok, dep)
        word=tok.text
        word=word.replace("'", "")
        #print (word)
        if dep==False and tok.ent_type_ in labels:
            nouns.append(word)

    nouns=str(nouns)
    nouns=nouns.replace("'", "")
    nouns=nouns.strip("[").strip(']')

    wordcloud= WordCloud(collocations=False, min_word_length=3, scale=4, background_color='white', ).generate(str(nouns))
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)