from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from config import Config
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, vector_store):
        
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-3.5-turbo",          # ✅ model_name → model
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI Assistant. Answer the user's questions strictly using the provided context below:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        retriever = vector_store.db.as_retriever(search_kwargs={"k": 4})
        base_rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        self.history = ChatMessageHistory()
        
        self.chain = RunnableWithMessageHistory(
            base_rag_chain,
            get_session_history=lambda session_id: self.history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"     # ✅ output_keys=[...] → output_messages_key
        )

    def get_response(self, query):
        try:
            logger.debug(f"Processing query: {query}")
            response = self.chain.invoke(
                {"input": query},
                config={"configurable": {"session_id": "local_chat"}}
            )
            return response['answer']
            
        except Exception as e:
            logger.error(f"❌ LLM Error: {str(e)}")
            return "I encountered an error processing your request. Please ensure your documents are vectorized."