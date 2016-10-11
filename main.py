import sys, time, hashlib, os, re
from tinydb import TinyDB, where, Query

def clearScreen():
    try:
        os.system("clear")
    except:
        os.system("cls")

def inputStudent():
    clearScreen()
    db = TinyDB('students.json')
    students = Query()
    fName = raw_input("Students First Name: ")
    lName = raw_input("Students Last Name: ")
    grade = raw_input("Grade Level: ")

    fName = re.sub('[^A-Za-z0-9]+', '', fName)
    lName = re.sub('[^A-Za-z0-9]+', '', lName)
    grade = re.sub('[^0-9]+', '', grade)

    userExists = db.count((students.firstName == fName) & (students.lastName == lName))
    if userExists < 1:
        studentId = str(fName)+" "+str(lName)+" "+str(grade)
        print("Please confirm the following is correct:")
        print("Name: %s %s") % (fName, lName)
        print("Grade: %s") % grade

        a = raw_input("Is the student information correct? [Y/N]")

        if a == "y" or a == "Y":
            if db.insert({'firstName':fName.upper(),'lastName':lName.upper(),'date':time.strftime("%d/%m/%Y"),'grade':grade,'barcode':studentId.upper()}):
                print(fName + " " + lName + " " + "saved!")
            else:
                print("ERROR: Could not save student.")
        else:
            inputStudent()
    else:
        print("ERROR: Student already exists...")

    raw_input("Press Enter to continue...")
    mainMenu()

def genBarcodes():
    import webbrowser
    clearScreen()
    #Create an HTML file that pulls the barcodes images down from a website.
    f = open('barcodes.html', 'w')

    db = TinyDB('students.json')

    allStudents = db.all()
    barcodes = []

    for student in allStudents:
        barcode = "<img src='http://barcode.advational.com/barcode.php?text=%s&print=true&size=50'>" % student["barcode"]
        barcodes.append(barcode)

    splitList = []
    for i in range(0, len(barcodes), 3):
        chunk = barcodes[i:i + 3]
        splitList.append(chunk)

    f.write("""<html><head><title>Barcodes</title></head><body onload="window.print()"><table width="100%" style="">""")
    for row in splitList:
        f.write("""<tr>""")
        for barcode in row:
            f.write("""<td style="text-align:center; padding-top:20px; border:1px #ccc dotted;">""")
            f.write(barcode)
            f.write("""</td>""")
        f.write("""</tr>""")
    f.write("""</table></body></html>""")
    f.close()
    print("Barcode file generated!!")
    print("Opening web browser")
    webbrowser.open("barcodes.html")
    time.sleep(0.5)
    clearScreen()
    mainMenu()

def editStudent():
    clearScreen()
    print("=== Edit Student ===")
    print("")
    print("1: Find by barcode")
    print("2: Find by name [NOT WORKING]")
    print("")
    print("0: Back to Main Menu")
    print("")
    mode = raw_input("Select a menu option: ")

    if(mode == '1'):
        editStudentByBarcode()
    elif(mode == '2'):
        editStudent()
    elif(mode == '0'):
        mainMenu()
    else:
        editStudent()

def editStudentByBarcode():
    clearScreen()
    print("=== Edit Student ===")
    print("")
    db = TinyDB('students.json')
    students = Query()
    scannedBarcode = raw_input("Search by barcode: ")
    print("Looking for: %s") % scannedBarcode.upper()
    try:
        student = db.get(students.barcode == scannedBarcode.upper())
        oldFname = student['firstName']
        oldLname = student['lastName']
        oldGrade = student['grade']

        fNameString = "First Name (%s)" % oldFname
        lNameString = "Last Name (%s)" % oldLname
        gradeString = "Grade (%s)" % oldGrade

        fName = raw_input(fNameString + ": ")
        lName = raw_input(lNameString + ": ")
        grade = raw_input(gradeString + ": ")

        if fName != "" and lName != "" and grade != "":
            studentId = str(fName)+str(lName)+str(grade)
            db.update({'firstName': fName.upper(),'lastName': lName.upper(),'grade':grade,'barcode':studentId.upper()}, students.barcode == scannedBarcode.upper())
            print "Student record updated"
        else:
            print "Unable to update record. All fields are required."
            raw_input("Press Enter to continue...")
            editStudent()
    except:
        print "ERROR: Unable to find student record..."

    raw_input("Press Enter to continue...")
    mainMenu()

def editStudentByName():
    pass

def remove():
    clearScreen()
    db = TinyDB('students.json')
    students = Query()
    fName = raw_input("First Name: ").upper()
    lName = raw_input("Last Name: ").upper()

    print("Looking for: %s %s") % (fName,lName)
    try:
        student = db.get(students.firstName == fName and students.lastName == lName)
        sBarcode = student['barcode']
        oldFname = student['firstName']
        oldLname = student['lastName']
        oldGrade = student['grade']
        print("Found student: %s %s in grade %s with barcode of %s") % (oldFname,oldLname,oldGrade,sBarcode)

        a = raw_input("Would you like to remove this student? [Y/N]: ")
        if a == "Y" or a == "y":
            db.remove(students.barcode == sBarcode)
            print("Student removed")
            raw_input("Press Enter to continue...")
            mainMenu()
        else:
            clearScreen()
            mainMenu()
    except:
        print("Student record could not be found...")
        raw_input("Press Enter to continue...")
        mainMenu()

def search():
    pass

def attendance(msg):
    clearScreen()
    print("=== Attendance ===")
    print("Type 'EXIT' for the main menu.")
    print("")
    print(msg)
    print("")
    studentDB = TinyDB('students.json')
    student = Query()
    barcode = raw_input("Barcode: ").upper()

    if barcode == "EXIT":
        mainMenu()
    else:
        exists = studentDB.count((student.barcode == barcode))
        if exists >= 1:
            studentData = studentDB.get(student.barcode == barcode)
            fName = str(studentData['firstName'])
            lName = str(studentData['lastName'])
            barcode = str(studentData['barcode'])
            attendanceDB = TinyDB('attendance.json')
            timeString = str(time.strftime("%d-%m-%Y_%H:%I:%S"))
            attendanceDB.insert({"firstName":fName,"lastName":lName,"barcode":barcode,"date":timeString})
            msg = "%s %s checked in!" % (str(fName),str(lName))
        else:
            msg = "ERROR: Could not find student record..."
    attendance(msg)

def mainMenu():
    clearScreen()

    print("=== Main Menu ===")
    print("")
    print("1: Take Attendance")
    print("2: Add Student")
    print("3: Edit Student [KINDA WORKING]")
    print("4: Remove Student")
    print("5: Search [NOT WORKING]")
    print("6: Print Barcodes [Internet connection required]")
    print("7: Report [NOT WORKING]")
    print("")
    print("0: Exit")
    print("")
    mode = raw_input("Select a menu option: ")

    if(mode == '1'):
        attendance("Ready for input")
    elif(mode == '2'):
        inputStudent()
    elif(mode == '3'):
        editStudent()
    elif(mode == '4'):
        remove()
    elif(mode == '5'):
        mainMenu()
    elif(mode == '6'):
        genBarcodes()
    elif(mode == '7'):
        mainMenu()
    elif(mode == '0'):
        clearScreen()
        exit(0)
    else:
        mainMenu()

mainMenu()