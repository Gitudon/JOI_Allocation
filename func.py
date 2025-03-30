import streamlit as st
import pandas as pd
from CONSTS import *

def message():
    st.title("JOIチューター割り当てアプリ")
    st.write("希望を元にチューターを各コースに割り当てます。")

def input_tutors() -> list:
    st.subheader("参加チューター")
    tutors = st.text_input("名前をカンマ区切りで入力 例: A, B, C")
    tutors = tutors.split(",")
    tutors = sorted([t.strip() for t in tutors])
    return tutors

def input_courses() -> list:
    st.subheader("開講コース")
    open_courses = st.multiselect("開講コースを選択", options=COURSES)
    return open_courses

def input_num_applicants(course:str, tutors:list) -> dict:
    st.subheader(course+"コース")
    num = st.number_input(f"割り当て人数({course})", min_value=0, max_value=5, value=0, step=1)
    applicants = st.multiselect(f"チューター希望者({course})", options=tutors)
    return {"num": num, "applicants": applicants}

def input_data(open_courses:list, tutors:list) -> dict:
    data = {}
    for course in open_courses:
        data[course] = input_num_applicants(course, tutors)
    return data

def convert_applicants_data(data:dict) -> dict:
    converted_applicants_data = {}
    for course in data.keys():
        applicants = data[course]["applicants"]
        for applicant in applicants:
            if applicant not in converted_applicants_data:
                converted_applicants_data[applicant] = []
            converted_applicants_data[applicant].append(course)
    return converted_applicants_data

def convert_num_data(data:dict) -> dict:
    converted_num_data = {}
    for course in data.keys():
        converted_num_data[course] = data[course]["num"]
    return converted_num_data

def allocate(converted_applicants_data:dict, converted_num_data:dict) -> dict:
    allocated_data = {}
    for course in converted_num_data.keys():
        allocated_data[course] = []
    while converted_applicants_data != {}:
        min_num = INF
        allocated_people = []
        allocated_courses = []
        for applicant in converted_applicants_data.keys():
            num = len(converted_applicants_data[applicant])
            if num < min_num:
                min_num = num
        for applicant in converted_applicants_data.keys():
            if applicant in allocated_people:
                continue
            if len(converted_applicants_data[applicant]) == min_num:
                for course in converted_applicants_data[applicant]:
                    if course in allocated_courses:
                        continue
                    allocated_course = course
                if len(allocated_data[allocated_course]) < converted_num_data[allocated_course]:
                    allocated_data[allocated_course].append(applicant)
                    allocated_people.append(applicant)
                    allocated_courses.append(allocated_course)
        delete_course_list = []
        for course in allocated_data.keys():
            if len(allocated_data[course]) == converted_num_data[course]:
                delete_course_list.append(course)
        for delete_course in delete_course_list:
            for applicant in converted_applicants_data.keys():
                if delete_course in converted_applicants_data[applicant]:
                    converted_applicants_data[applicant].remove(delete_course)
        delete_person_list = []
        for applicant in converted_applicants_data.keys():
            if len(converted_applicants_data[applicant]) == 0:
                delete_person_list.append(applicant)
        for delete in delete_person_list:
            del converted_applicants_data[delete]
    for allocated in allocated_data.keys():
        allocated_data[allocated] = list(set(allocated_data[allocated]))
    return allocated_data

def make_a_table(allocated_data:dict) -> pd.DataFrame:
    df = pd.DataFrame(allocated_data).T
    df.columns = ["チューター"]
    df.index.name = "コース"
    return df.reset_index()

def show_a_table(df:pd.DataFrame) -> None:
    st.subheader("割り当て結果")
    st.dataframe(
        df,
        hide_index=True,
        column_config={
        }
    )