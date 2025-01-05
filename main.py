import streamlit as st
from crewai.flow.flow import Flow, listen, start
from litellm import completion
import json
import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


class DebateFlow(Flow):
    model = "gpt-4o-mini"
    def __init__(self, topic="the benefits of AI"):  #adding default topic
        super().__init__()
        self.topic = topic

    @start()
    def opening_argument(self):
      response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Initiate the Debate dicsussion by providing arguments in support of {self.topic}. Provide justifications and examples to make them effective.",
                },
            ],
        )

      argument_response = response["choices"][0]["message"]["content"]
      print("Arguments in favour:")
      print(argument_response)
      return argument_response

    @listen(opening_argument)
    def counter_argument(self, support_response):
      response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Provide arguments in opposition to {self.topic}. Counter the previous arguments. Provide justifications and examples to make them effective. ",
                },
            ],
        )

      argument_response = response["choices"][0]["message"]["content"]
      debate_discussion = {"support_response": support_response, "counter_response": argument_response}
      print("Arguments against")
      return json.dumps(debate_discussion)
# Streamlit application
def main():
    st.title("Debate Chat Application")
    
    # User input for the debate topic
    topic = st.text_input("Enter the debate topic:", "the benefits of AI")
    
    if st.button("Start Debate"):
        debate_flow = DebateFlow(topic)
        response = debate_flow.kickoff()
        response = json.loads(response)
        # Displaying the conversation
        st.subheader("Chat Conversation")
        st.write("**Student 1:** Arguments in favor:")
        st.write(response["support_response"])
        st.write("**Student 2:** Arguments against:")
        st.write(response["counter_response"])

if __name__ == "__main__":
    main()
