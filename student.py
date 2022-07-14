# ----------------------------------------------------------------
# Michael Nolan
# 29 June 2022
# This module supports changes in the registered courses
# for students in the class registration system.  It allows
# students to add courses, drop courses and list courses they are
# registered for.
# -----------------------------------------------------------------


def list_courses(id, c_roster):
    # ------------------------------------------------------------
    # This function displays and counts courses a student has
    # registered for.  It has two parameters: id is the ID of the
    # student; c_roster is the list of class rosters. This function
    # has no return value.
    # -------------------------------------------------------------

    # Heading
    print("Courses Registered:")

    # The variable Counter is used to count how many classes a student is signed up for.
    counter = 0

    # Use a for loop to see which classes a student is in
    for course in c_roster:
        # print(courses)
        # print(students)
        if id in c_roster[course]:
            print(course)
            counter += 1
    print(f"Total number: {counter}")


def add_course(id, c_roster, c_max_size, force=False):
    # ------------------------------------------------------------
    # This function adds a student to a course.  It has three
    # parameters: id is the ID of the student to be added; c_roster is the
    # list of class rosters; c_max_size is the list of maximum class sizes.
    # force, if true, will bypass course size restrictions.
    # This function asks user to enter the course he/she wants to add.
    # If the course is not offered, display error message and stop.
    # If student has already registered for this course, display
    # error message and stop.
    # If the course is full, display error message and stop.
    # If everything is okay, add student ID to the course’s
    # roster and display a message if there is no problem.  This
    # function has no return value.
    # -------------------------------------------------------------

    # Asks user for desired course
    desired_course = input("Enter desired course: ").upper()

    # Checks if user input is a class
    if desired_course not in c_roster.keys():
        print("Course not found.")
        return

    # Checks if student is already enrolled in their inputted course
    if id in c_roster[desired_course]:
        print("You are already enrolled in that course.")
        return

    # Counts how many students are in a class and checks if it matches the max amount
    if not force and len(c_roster[desired_course]) >= c_max_size[desired_course]:
        print("Course already full.")
        return

    # Everything OK. Add student to the course
    print("Course added.")
    c_roster[desired_course].append(id)


def drop_course(id, c_roster):
    # ------------------------------------------------------------
    # This function drops a student from a course.  It has two
    # parameters: id is the ID of the student to be dropped;
    # c_roster is the list of class rosters. This function asks
    # the user to enter the course he/she wants to drop.  If the course
    # is not offered, display error message and stop.  If the student
    # is not enrolled in that course, display error message and stop.
    # Remove student ID from the course’s roster and display a message
    # if there is no problem.  This function has no return value.
    # -------------------------------------------------------------

    # Asks user for course to drop
    desired_course = input("Enter course: ").upper()

    # Checks if user input is a class
    if desired_course not in c_roster.keys():
        print("Course not found.")
        return

    # Checks if student is enrolled in their inputted course, display error if not
    if id not in c_roster[desired_course]:
        print("You are not enrolled in that course.")
        return

    # No problem, remove student from course roster
    print("Course dropped.")
    c_roster[desired_course].remove(id)