import streamlit as st
from func import *

def main():
    message()
    open_courses = input_courses()
    tutors = input_tutors()
    data = input_data(open_courses,tutors)
    converted_applicants_data = convert_applicants_data(data)
    converted_num_data = convert_num_data(data)
    if st.button("割り当て開始"):
        show_a_table(make_a_table(allocate(converted_applicants_data, converted_num_data)))

if __name__=="__main__":
    main()