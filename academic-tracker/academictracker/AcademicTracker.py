import json
student = {}


while True:
    print("-"*10 + "Student Evualtion Sytem " + "-" *10)
    print("1. Add Student")
    print("2. View Student")
    print("3. Exit")
    choice = input("enter ur choice : ")

    if choice == '1':
        name = input("enter student name")
        age = input("enter student age")
        grade = input("enter student grade")
        major = input("enter student major")
        note = input("enter student note")
        student[name] = {
             "age" : age , 
             "grade" : grade ,
              "major" : major ,
               "note" : note }
        with open ("academictracker.json", "w") as f :
             json.dump (student , f)


    elif choice == '2':
            with open ("academictracker.json","r") as f:
                 student = json.load(f)
            for name, inf in student.items():
                        print("Name:", name)
                        print("Age:", inf["age"])
                        print("Grade:", inf["grade"])
                        print("Major:", inf["major"])
                        print("Note:", inf["note"])
                        print("-"*10)
                 

    elif choice == '3':
          print("exiting...")
          break 