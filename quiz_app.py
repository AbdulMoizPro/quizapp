import streamlit as st
import time

# Function to calculate the time taken
def start_timer():
    start_time = time.time()
    return start_time

def main():
    # Initialize the session state if it doesn't exist yet
    if 'questions' not in st.session_state:
        st.session_state['questions'] = []

    # Timer control flag
    if 'timer_started' not in st.session_state:
        st.session_state['timer_started'] = True

    # Sidebar for creating questions
    st.sidebar.title("Create Your Questions")

    # Input fields for question and number of options
    question = st.sidebar.text_input("Enter your question:")
    num_options = st.sidebar.number_input("How many options?", min_value=2, max_value=6, value=4, step=1)

    # Create empty list for options dynamically based on the number
    options = []
    for i in range(num_options):
        option_text = st.sidebar.text_input(f"Option {i+1}:", key=f"option_{i}")
        if option_text:
            options.append(option_text)
    
    # Correct answer selection (must be one of the options)
    correct_answer = st.sidebar.selectbox("Select the correct answer:", options)

    # Add question button
    if st.sidebar.button("Add Question"):
        # Append the question and its options to the list in session state
        if question and len(options) == num_options:
            st.session_state['questions'].append({
                "question": question,
                "options": options,
                "answer": correct_answer
            })
            st.sidebar.success("Question added successfully!")
        else:
            st.sidebar.error("Please fill in all fields!")

    # Display added questions in the sidebar (if any)
    if st.session_state['questions']:
        st.sidebar.subheader("Your Added Questions")
        for idx, q in enumerate(st.session_state['questions']):
            st.sidebar.write(f"Q{idx+1}: {q['question']}")

    # Main quiz section
    if st.session_state['questions']:
        st.title("Quiz App")

        # Start Timer button
        if st.button("Start Timer"):
            st.session_state['timer_started'] = True
            st.session_state['start_time'] = start_timer()
            st.success("Timer started!")

        if st.session_state['timer_started']:
            # Question counter
            score = 0
            user_answers = []

            # Loop through the questions
            for idx, q in enumerate(st.session_state['questions']):
                st.subheader(f"Q{idx + 1}: {q['question']}")

                # Display options as radio buttons
                user_answer = st.radio(f"Select an answer for question {idx + 1}:", q['options'], key=f"q{idx}")
                user_answers.append(user_answer)

                # Check if an answer was selected
                if user_answer:
                    # Check if the answer is correct
                    if user_answer == q['answer']:
                        score += 1

            # Show the results (Score and Time)
            if st.button("Submit Quiz"):
                end_time = time.time()
                total_time = round(end_time - st.session_state['start_time'], 2)

                # Simulate a popup-like effect by using an Expander
                with st.expander("Quiz Results"):
                    st.write(f"**Your score: {score}/{len(st.session_state['questions'])}**")
                    st.write(f"**Time taken: {total_time} seconds**")

                    # Display correct answers for each question
                    for idx, q in enumerate(st.session_state['questions']):
                        if user_answers[idx] != q['answer']:
                            st.write(f"**Q{idx + 1}:** {q['question']}")
                            st.write(f"Your answer: {user_answers[idx]}")
                            st.write(f"Correct answer: {q['answer']}")
                        else:
                            st.write(f"**Q{idx + 1}:** {q['question']}")
                            st.write(f"Your answer: {user_answers[idx]} (Correct!)")

if __name__ == "__main__":
    main()
