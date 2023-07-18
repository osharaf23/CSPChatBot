
import streamlit as st
import csv
from es_test import test, save_to_csv

header = st.container()
input = st.container()
llm_out = st.container()
es_out = st.container()
hr_out = st.container()

input_val = ""

with header:
    st.title('CSP Prompt Interface--Omar')

with input:
    input_val = input.text_input('Ask your database a prompt!')

if input_val:

    results = test(input_val)
    # print(results)

    with llm_out:
        st.header('LLM Output (user prompt -> ES query)')
        st.write(results[1])

    with es_out:
        st.header('ES Output (ES query -> ES response)')
        st.write(results[2])


    with hr_out:
        st.header('Human Readable Output (ES response -> Human Readable response)')
        st.write(results[3])

    save_to_csv([results], 'es-llm-data.csv')