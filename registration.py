# ----------------------------------------------------------------
# Author: Joel Howell
# Date: 6/30/2022
#
# This program creates a class registration system.  It allows
# students to add courses, drop courses and list courses they are
# registered for. It also allows students to review the tuition
# costs for their course roster.
# -----------------------------------------------------------------
import student
import billing
import pickle

# path to roster file
SAVE_PATH = 'roster.dat'


def main():
    # ------------------------------------------------------------
    # This function manages the whole registration system.  It has
    # no parameter.  It creates student list, in_state_list, course
    # list, max class size list and roster list.  It uses a loop to
    # serve multiple students. Inside the loop, ask student to enter
    # ID, and call the login function to verify student's identity.
    # Then let student choose to add course, drop course or list
    # courses. This function has no return value.
    # -------------------------------------------------------------

    student_list = [('1001', '111'), ('1002', '222'),
                    ('1003', '333'), ('1004', '444')]
    admin_list = [('admin', '12345')]

    student_in_state = {'1001': True,
                        '1002': False,
                        '1003': True,
                        '1004': False}

    course_hours = {'CSC101': 3, 'CSC102': 4, 'CSC103': 5, 'CSC104': 3}
    course_roster = load_roster()
    # course_roster = {'CSC101': ['1004', '1003'],
    #                  'CSC102': ['1001'],
    #                  'CSC103': ['1002'],
    #                  'CSC104': []}

    course_max_size = {'CSC101': 3, 'CSC102': 2, 'CSC103': 1, 'CSC104': 3}

    while True:
        while True:
            id = input("Enter ID to login, or 0 to save & quit: ")
            if id == '0':
                save_roster(course_roster)
                exit()
            if login(id, student_list, admin_list):
                # login success
                is_admin = id in [user[0] for user in admin_list]
                break
            else:
                # login failure
                continue

        if is_admin:
            admin_menu(id, student_list, course_roster, course_max_size, student_in_state, course_hours)
        else:
            student_menu(id, course_roster, course_max_size, student_in_state, course_hours)


def load_roster(force_defaults=False):
    # ------------------------------------------------------------
    # This function loads the course roster from text file.
    # Takes parameter force_defaults. Defaults are always used if true. Otherwise,
    # if the file does exist, the file loads and returns the values.
    # If the file does not exist, it returns default values.
    # ------------------------------------------------------------
    default_data = {'CSC101': ['1004', '1003'], 'CSC102': ['1001'], 'CSC103': ['1002'], 'CSC104': []}

    if force_defaults:
        return default_data
    try:
        with open(SAVE_PATH, "rb") as f:
            data = pickle.load(f)
            print("Course roster loaded successfully.\n")
    except FileNotFoundError:
        print("Course roster does not exist.")
        print("Loading default values...\n")
        data = default_data
    return data


def save_roster(course_roster):
    # ------------------------------------------------------------
    # This function writes the course roster to text file.
    # It has one parameter, course_roster
    # ------------------------------------------------------------
    with open(SAVE_PATH, "wb") as f:
        pickle.dump(course_roster, f)
    print("\nCourse roster saved successfully.")


def login(id, s_list, a_list):
    # ------------------------------------------------------------
    # This function allows a student or admin to log in.
    # It has three parameters:
    # id: student id
    # s_list: student list
    # a_list: admin list
    # This function asks user to enter PIN. If the ID and PIN
    # combination is in s_list or a_list, display message of verification and
    # return True. Otherwise, display error message and return False.
    # -------------------------------------------------------------

    pin = input("Enter PIN: ")

    if (id, pin) in s_list + a_list:
        print("ID and PIN verified.")
        return True
    else:
        print("ID or PIN incorrect.\n")
        return False


def admin_menu(admin_id, student_list, course_roster, course_max_size, student_in_state, course_hours):
    # ------------------------------------------------------------
    # This function provides the interactive menu for admins.
    # Parameters:
    # admin_id: admin ID
    # student_list: List of student credentials.
    # course_roster: Dict of class:students pairs.
    # course_max_size: Dict of class:size pairs.
    # student_in_state: Dict of student:bool pairs.
    # course_hours: Dict of course:hours pairs.
    #
    # Prompts an admin, letting them log in as a student,
    # force-add a student to a class,
    # or remove a student from a class.
    # ------------------------------------------------------------
    print(f'Admin menu. Logged in as "{admin_id}".')
    while True:
        x = input(
            'Enter 1 to log in as a student, 2 to force-add a student to a class, 3 to remove a student from a class, 4 to list the classes of a student, 5 to return roster to defaults, 0 to exit: ')
        if x == '0':
            # exit
            print('Admin session ended.')
            break
        elif x == '1':
            # login as student
            while 1:
                y = input('Enter student ID to log in as: ')
                if y in [user[0] for user in student_list]:
                    student_menu(y, course_roster, course_max_size, student_in_state, course_hours)
                    break
                else:
                    print('Student ID not found.')
        elif x == '2':
            # force-add student to class
            while 1:
                y = input('Enter student ID to add to a course: ')
                if y in [user[0] for user in student_list]:
                    # student.add_course does some checks of its own. disable size restriction checking
                    student.add_course(y, course_roster, course_max_size, force=True)
                    break
                else:
                    print('Student ID not found.')
        elif x == '3':
            # remove student from class
            while 1:
                y = input('Enter student ID to remove from a course: ')
                if y in [user[0] for user in student_list]:
                    student.drop_course(y, course_roster)
                    break
                else:
                    print('Student ID not found.')
        elif x == '4':
            # check student's courses
            while 1:
                y = input('Enter ID of student to list classes: ')
                if y in [user[0] for user in student_list]:
                    student.list_courses(y, course_roster)
                    break
                else:
                    print('Student ID not found.')
        elif x == '5':
            # mutate course_roster instead of assigning to avoid creating a local version
            course_roster |= load_roster(force_defaults=True)
            print('Roster overwritten with defaults.\n')
            continue
        else:
            print('Unknown input.')
            continue


def student_menu(id, course_roster, course_max_size, student_in_state, course_hours):
    # ------------------------------------------------------------
    # This function provides the interactive menu for students.
    # Parameters:
    # id: Student ID
    # course_roster: Dict of class:students pairs.
    # course_max_size: Dict of class:size pairs.
    # student_in_state: Dict of student:bool pairs.
    # course_hours: Dict of course:hours pairs.
    #
    # Prompts a student, letting them add a course,
    # drop a course, list their courses, or show their bill.
    # ------------------------------------------------------------
    print(f'Logged in as student {id}.')
    while True:
        x = input("\nEnter 1 to add course, 2 to drop course, 3 to list courses, 4 to show bill, 0 to exit: ")
        if x == '0':
            print("Student session ended.")
            break
        elif x == '1':
            student.add_course(id, course_roster, course_max_size)
        elif x == '2':
            student.drop_course(id, course_roster)
        elif x == '3':
            student.list_courses(id, course_roster)
        elif x == '4':
            credit_hours, total_cost = billing.calculate_hours_and_bill(id, student_in_state, course_roster,
                                                                        course_hours)
            billing.display_hours_and_bill(credit_hours, total_cost)
        else:
            print("Unknown input.")
            continue


main()