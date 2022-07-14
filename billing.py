# ----------------------------------------------------------------
# Author: Shane Galvin for Group 1
# Date: 2022-06-29
#
# This module calculates and displays billing information
# for students in the class registration system.  Student and
# class records are reviewed and tuition fees are calculated.
# -----------------------------------------------------------------

COST_CREDITHR_INSTATE = 225  # cost per credit-hour for in-state students
COST_CREDITHR_OUTSTATE = 850  # cost per credit-hour for out-of-state students


def calculate_hours_and_bill(id, s_in_state, c_rosters, c_hours):
    # ------------------------------------------------------------
    # This function calculate billing information. It takes four
    # parameters: id, the student id; s_in_state, the list of
    # in-state students; c_rosters, the rosters of students in
    # each course; c_hours, the number of hours in each course.
    # This function returns the number of course hours and tuition
    # cost.
    # ------------------------------------------------------------

    in_state = s_in_state[id]  # is the student in-state?
    cost_credithr = COST_CREDITHR_INSTATE if in_state else COST_CREDITHR_OUTSTATE  # cost per credit-hour for student

    total_credithr = 0
    total_cost = 0

    for course, roster in c_rosters.items():
        if id in roster:
            course_credithr = c_hours[course]
            total_credithr += course_credithr
            total_cost += cost_credithr * course_credithr

    return total_credithr, total_cost


def display_hours_and_bill(hours, cost):
    # ------------------------------------------------------------
    # This function prints the number of course hours the student
    # is taking and the total tuition cost. It takes two parameters:
    # hours and cost. This function has no return value.
    # ------------------------------------------------------------
    print(f'Course load: {hours} credit hours')
    print(f'Enrollment cost: ${cost:.2f}')