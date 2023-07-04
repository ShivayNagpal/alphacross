import streamlit as st
import alphacross
import pandas as pd

#caching all major utility functions for streamlit app
@st.cache_data
def generate_words(theme,max_word_limit):
    return alphacross.generate_words(theme,max_word_limit)

@st.cache_data
def sort_according_to_rank(word_list,theme):
    return alphacross.sort_according_to_rank(word_list,theme)

@st.cache_data
def generate_clues(word_list,theme):
    return alphacross.generate_all_clues(word_list,theme)

@st.cache_data
def remove_ranks(list_of_words):
    return alphacross.remove_ranks(list_of_words)

st.set_page_config(page_title="alphaCross")
st.markdown("# alphaCross")
st.markdown("## Crossword Constructor Helper")

theme=st.text_input('Enter Theme',placeholder="eg. Mother's Day")
max_word_limit=st.number_input('Enter Max Word Length',value=8)

#declaring state variables
st.session_state.selected_words=[]
st.session_state.final_dict={}

submit=st.button('Submit')
if 'submit' in st.session_state:
    submit=st.session_state.submit

if submit:
    st.session_state.submit=True
    word_list=generate_words(theme,max_word_limit)#generating words
    word_list=sort_according_to_rank(word_list,theme)#sorting words

    st.session_state.selected_words = st.multiselect('Select ranked words', word_list)#selecting words

    clue_gen=st.button('Proceed to clue generation')
    if 'clue_gen' in st.session_state:
        clue_gen=st.session_state.clue_gen

    if clue_gen:
        #genrating clues after removing ranks from strings
        st.session_state.final_dict=generate_clues(remove_ranks(st.session_state.selected_words),theme)

        #displaying results
        st.dataframe(pd.DataFrame({'Words':st.session_state.final_dict.keys(),'Clues':st.session_state.final_dict.values()}))