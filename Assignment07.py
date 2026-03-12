# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   x,1/1/2026,Created Script
#   x,3/11/2026,Modified script to meet requirements of assignment 7.
# ------------------------------------------------------------------------------------------ #
import json
import _io

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str = ""  # Hold the choice made by the user.


# Person Class
class Person:
    """
    A class representing person data.

    Properties:
        first_name (str): The student's first name.
        last_name (str): The student's last name.

    ChangeLog:
        - x,3.11.2026,Created Class
    """
    def __init__(self, first_name: str = '', last_name: str = ''):
        """ Constructor for the Person class

        ChangeLog:
            - x,3.11.2026,Created Constructor

        :param first_name: The person's first name
        :param last_name: The person's last name
        """
        self.first_name = first_name  
        self.last_name = last_name

    @property  # (Use this decorator for the getter or accessor)
    def first_name(self):
        """ Getter/accessor for the first_name property.

        ChangeLog:
            - x,3.11.2026,Created Getter

        :return: The person's first name formatted with title case
        """
        return self.__first_name.title() 

    @first_name.setter
    def first_name(self, value: str):
        """ Setter/mutator for the first_name property.
        Makes sure that the first name does not contain numbers.

        ChangeLog:
            - x,3.11.2026,Created Setter

        :param value: The new first name value
        :raises ValueError: If the value contains non-alphabetic characters
        """
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def last_name(self):
        """ Getter/accessor for the last_name property.

        ChangeLog:
            - x,3.11.2026,Created Getter

        :return: The person's last name formatted with title case
        """
        return self.__last_name.title()  

    @last_name.setter
    def last_name(self, value: str):
        """ Setter/mutator for the last_name property.
        Makes sure that the last name does not contain numbers.

        ChangeLog:
            - x,3.11.2026,Created Setter

        :param value: The new last name value
        :raises ValueError: If the value contains non-alphabetic characters
        """
        if value.isalpha() or value == "":  # is alphabetic or empty string
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self) -> str:
        """ Overrides the default __str__() method to return a comma-separated string.

        ChangeLog:
            - x,3.11.2026,Created method
        """
        return f'{self.first_name},{self.last_name}'


# Student Class (inherits from Person)
class Student(Person):
    """
    A class representing student data, inheriting from the Person class.

    Properties:
        first_name (str): Inherited from Person.
        last_name (str): Inherited from Person.
        course_name (str): The name of the course the student is enrolled in.

    ChangeLog:
        - x,3.11.2026,Created Class
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        """ Constructor for the Student class.
        Passes first_name and last_name up to the Person constructor via super().

        ChangeLog:
            - x,3.11.2026. Created Constructor

        :param first_name: The student's first name
        :param last_name: The student's last name
        :param course_name: The name of the course the student is enrolled in
        """
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name  # uses setter for validation

    @property
    def course_name(self):
        """ Getter/accessor for the course_name property.

        ChangeLog:
            - x,3.11.2026,Created Getter

        :return: The course name string
        """
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        """ Setter/mutator for the course_name property.
        Ensures the course name is not empty.

        ChangeLog:
            - x,3.11.2026,Created Setter

        :param value: The new course name value
        :raises ValueError: If the value is an empty string
        """
        if value.strip() or value == "":  # has content or is empty string
            self.__course_name = value
        else:
            raise ValueError("The course name should not be blank.")

    def __str__(self) -> str:
        """ Overrides the Person __str__() method to include course_name.

        ChangeLog:
            - x,3.11.2026,Created method
        """
        return f'{self.first_name},{self.last_name},{self.course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    x,1.1.2030,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of Student objects
        then returns the list filled with student data.

        ChangeLog: (Who, When, What)
        x,1.1.2030,Created function
        x,3.11.2026,Updated to build Student objects from JSON dicts

        :param file_name: string data with name of file to read from
        :param student_data: list to populate with student data

        :return: list of Student objects
        """
        file = None
        try:
            file = open(file_name, "r")
            json_students = json.load(file)

            # Convert list of dicts to list of Student objects
            student_objects = []
            for dict_student in json_students:
                student = Student(
                    dict_student['FirstName'],
                    dict_student['LastName'],
                    dict_student['CourseName']
                )
                student_objects.append(student)
            student_data.clear()
            student_data.extend(student_objects)

        except Exception as e:
            IO.output_error_messages(
                message="Error: There was a problem with reading the file.", error=e
            )
        finally:
            if file is not None and not file.closed:
                file.close()

        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of Student objects.

        ChangeLog: (Who, When, What)
        x,1.1.2030,Created function
        x,3.11.2026,Added conversion of Student objects to dicts before writing

        :param file_name: string data with name of file to write to
        :param student_data: list of Student objects to be written to the file

        :return: None
        """
        file = None
        try:
            # Convert Student objects into dictionaries
            dict_students = []
            for student in student_data:
                student_json = {
                    "FirstName": student.first_name,
                    "LastName": student.last_name,
                    "CourseName": student.course_name
                }
                dict_students.append(student_json)

            file = open(file_name, "w")
            json.dump(dict_students, file, indent=2)

            IO.output_student_courses(student_data=student_data)

        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file is not None and not file.closed:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    x,1.1.2030,Created Class
    x,1.2.2030,Added menu output and input functions
    x,1.3.2030,Added a function to display the data
    x,1.4.2030,Added a function to display custom error messages
    x,3.11.2026,Renamed output_student_and_course_names to output_student_courses,
                         updated to use Student class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays a custom error message to the user.

        ChangeLog: (Who, When, What)
        x,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user.

        ChangeLog: (Who, When, What)
        x,1.1.2030,Created function

        :param menu: string containing the menu text

        :return: None
        """
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        x,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the student and course names to the user as
        comma-separated values.

        ChangeLog: (Who, When, What)
        x,1.1.2030,Created function
        x,3.11.2026,Renamed to output_student_courses and updated to use Student objects
        x,3.11.2026,Updated to print comma-separated values

        :param student_data: list of Student objects to be displayed

        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(student)
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name andlast name, with a course name from the user.

        ChangeLog: (Who, When, What)
        x,1.1.2030,Created function
        x,3.11.2026,Replaced dict with Student object

        :param student_data: list of Student objects to be filled with input data

        :return: list
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha() or student_first_name == "":
                raise ValueError("The first name should not contain numbers and should not be blank.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha() or student_last_name == "":
                raise ValueError("The last name should not contain numbers and should not be blank.")
            course_name = input("Please enter the name of the course: ")
            if course_name.strip() == "":
                raise ValueError("The course name should not be blank.")
            student = Student(student_first_name, student_last_name, course_name)
            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the incorrect type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of Student objects
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
