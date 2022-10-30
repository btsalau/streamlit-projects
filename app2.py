import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
import urllib.request 
import plotly.express as px

## Importing Image from GitHub


image_url = 'https://raw.githubusercontent.com/dataprofessor/streamlit_freecodecamp/main/app_2_simple_bioinformatics_dna/dna-logo.jpg'

urllib.request.urlretrieve(image_url, 'image.jpg')
image = Image.open('image.jpg')

## Adding Image to Streamlit App
st.image(image, use_column_width=True)

## Start writing Streamlit App Text Content
st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA

***
""")

# Using Streamlit's Magic Method
"### DNA Sequence Input"

input = ""
sample_sequence = "DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

# > - is like a markdown element - Blockquote

# Insert text field
dna_input = st.text_area("Input your DNA sequence", sample_sequence, height=250)

"## DNA Query"
"You have entered the following as your DNA Sequence:"

dna_input

'***'

"## DNA Composition Output"

"Now Processing..."
dna_input = dna_input.splitlines()
dna_input = dna_input[1:]
dna_sequence = ''.join(dna_input)

dna_sequence

def dna_composition(seq):
    composition = {}
    for i in seq:
        try:
            composition[i] += 1
        except KeyError:
            composition[i] = 1
    
    return composition

# Output 1
st.subheader("1. Print Dictionary Compositon")

X = dna_composition(dna_sequence)

X # could also use st.write

# Output 2
st.subheader("2. Print Text")

f'There are {X["G"]} guanine in the DNA.'
f'There are {X["A"]} adenine in the DNA.'
f'There are {X["T"]} thymine in the DNA.'
f'There are {X["C"]} cytosine in the DNA.'

# Output 3
st.subheader("3. Display Dataframe")

df = pd.DataFrame.from_dict(
    data=X,
    orient='index',
    columns=['count'])
df.reset_index(
    drop=False,
    inplace=True,
    names='nucleotide'
)

st.write(df)

# Output 4
st.subheader("4. Display Bar Chart Using Altair")

p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p = p.properties(
    width=alt.Step(80) # controls width of bar.
  )  

st.write(p)

# Output 5 - Try Plotly
st.subheader("Display Chart Using Plotly")

fig = px.bar(
    data_frame=df, 
    x='nucleotide', 
    y='count', 
    title="Count of Nucleotides in DNA Sequence"
    )

st.write(fig)