import streamlit as st

def display():
    st.header("ReguSync")
    st.write("ReguSync keeps you updated with the latest regulatory changes. Compare different versions of your documents to see what's changed.")

    uploaded_file1 = st.file_uploader("Upload the first version of your document", key="file1")
    uploaded_file2 = st.file_uploader("Upload the second version of your document", key="file2")

    if uploaded_file1 is not None and uploaded_file2 is not None:
        doc1 = uploaded_file1.read().decode("utf-8")
        doc2 = uploaded_file2.read().decode("utf-8")
        
        diff = difflib.HtmlDiff().make_file(doc1.splitlines(), doc2.splitlines(), 'Version 1', 'Version 2')
        st.markdown(diff, unsafe_allow_html=True)