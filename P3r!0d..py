import streamlit as st
import streamlit as st
import base64
import os
from groq import Groq
from pinecone import Pinecone, ServerlessSpec

os.environ["GROQ_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "e9549a8f-6384-4850-b05e-4dd6fdcd51d4"

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("quickstart")

st.session_state.api_key = os.environ.get("GROQ_API_KEY")

# Only show the API key input if the key is not already set
if not st.session_state.api_key:
    # Ask the user's API key if it doesn't exist
    api_key = st.text_input("Enter API Key", type="password")
    
    # Store the API key in the session state once provided
    if api_key:
        st.session_state.api_key = api_key
        st.rerun()  # Refresh the app once the key is entered to remove the input field
else:
    # If the API key exists, show the chat app
    
   

    # Inject CSS for background image and black text for the title
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://t3.ftcdn.net/jpg/06/37/22/56/360_F_637225687_YnecAmnWVNpmPyF506YIdJlwtBOCUDfr.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color:rgba(255,255,255,0.2);
            background-blend-mode: overlay;
            height: 100vh;
            width: 100vw;
        }
        
        .top-right {
            position: absolute;
            top: 2px;
            right: 0px;
            text-align: right;
        }
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: black !important;
            
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

    # Streamlit content with customized title text
    st.markdown("<div class='top-right'><h1>P3r!0d.</h1></div>", unsafe_allow_html=True)


    
  

    # Initialize the chat message list in session state if it doesn't exist
    if "chat_messages" not in st.session_state:
        st.session_state.groq_chat_messages = [{"role": "system", "content": "You are a helpful assistant. The user will ask a query, and you will respond to it. If any additional context for the query is found, you will be provided with it."}]
        st.session_state.chat_messages = []
        
    # Display previous chat messages
    for messages in st.session_state.chat_messages:
        if messages["role"] in ["user", "assistant"]:
            with st.chat_message(messages["role"]):
                st.markdown(messages["content"])
    
    # Define a function to simulate chat interaction (you would replace this with an actual API call)
    def get_chat():
        embedding = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[st.session_state.chat_messages[-1]["content"]],
            parameters={
                "input_type": "query"
            }
        )
        results = index.query(
            namespace="ns1",
            vector=embedding[0].values,
            top_k=3,
            include_values=False,
            include_metadata=True
        )
        context = ""
        for result in results.matches:
            if result['score'] > 0.8:
                context += result['metadata']['text']
            
        st.session_state.groq_chat_messages[-1]["content"] = f"User Query: {st.session_state.chat_messages[-1]['content']} \n Retrieved Content (optional): {context}"
        chat_completion = client.chat.completions.create(
            messages=st.session_state.groq_chat_messages,
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content

    # Handle user input
    if prompt := st.chat_input("Ask me anything, I am the P3r!0d. bot. I am precise. P3r!0d."):
        # Display user message
        t=prompt.lower()
        if ("women" in t and ("empowerment" in t or "resources" in t or "community support" in t or "support " in t or "tech" in t or "representation" in t or "learning" in t)):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            st.session_state.groq_chat_messages.append({"role": "user", "content": prompt})
            # Get the assistant's response (in this case, it's just echoing the prompt)
            with st.spinner("Getting responses..."):
                response = "Here are some resources from the internet that can help address the specific needs women have in online spaces:https://women-in-tech.org/"
        if ("women" in t and ("literacy" in t or "free coding" in t or "coding tutorial" in t or "coding" in t or "organisation" in t)):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            st.session_state.groq_chat_messages.append({"role": "user", "content": prompt})
            # Get the assistant's response (in this case, it's just echoing the prompt)
            with st.spinner("Getting responses..."):
                response = "Here are some resources from the internet that can help address the specific needs women have in online spaces:https://girlswhocode.com/"
        if ("women" in t and ("carrer" in t or "advise" in t or "network" in t or "community" in t or "organisation" in t)):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            st.session_state.groq_chat_messages.append({"role": "user", "content": prompt})
            # Get the assistant's response (in this case, it's just echoing the prompt)
            with st.spinner("Getting responses..."):
                response = "Here are some resources from the internet that can help address the specific needs women have in online spaces:https://elpha.com/"
            
               
            
        else:
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            st.session_state.groq_chat_messages.append({"role": "user", "content": prompt})
            # Get the assistant's response (in this case, it's just echoing the prompt)
            with st.spinner("Getting responses..."):
                response = get_chat()
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add user message and assistant response to chat history
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.session_state.groq_chat_messages.append({"role": "assistant", "content": response})
