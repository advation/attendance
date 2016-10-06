import sys, time, hashlib, os
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

    userExists = db.count((students.firstName == fName) & (students.lastName == lName))
    if userExists < 1:
        numStudentsInGrade = int(len(db))
        sNum = numStudentsInGrade + 1
        studentId = str(sNum)

        print("Please confirm the following is correct:")
        print("Name: %s %s") % (fName, lName)
        print("Grade: %s") % grade

        a = raw_input("Is the student information correct? [Y/N]")

        if a == "y" or a == "Y":
            if db.insert({'firstName':fName,'lastName':lName,'date':time.strftime("%d/%m/%Y"),'grade':grade,'barcode':studentId}):
                genBarcode(studentId, fName, lName)
                print(fName + " " + lName + " " + "saved!")
            else:
                print("ERROR: Could not save student.")
        else:
            inputStudent()
    else:
        print("ERROR: Student already exists...")

    raw_input("Press Enter to continue...")
    mainMenu()

def genBarcode(studentId,fName,lName):
    import barcode
    from barcode.writer import ImageWriter
    tn = barcode.get('code39',studentId, writer=ImageWriter())
    nameString = "barcodes/" + lName + "_" + fName
    tn.save(nameString)

def printAllBarcodes():
    clearScreen()
    try:
        os.system('montage -mode concatenate barcodes/*.png barcodes/barcodes.png')
        try:
            os.startfile("barcodes/barcodes.png","print")
        except:
            os.system("lpr barcodes/barcodes.png")
        os.system('rm barcodes/barcodes.png')
    except:
        pass

    #mainMenu()

def editStudent():
    clearScreen()

    print("=== Edit Student ===")
    print("1: Find by barcode")
    print("2: Find by name")
    print("3: Back to Main Menu")
    mode = raw_input("Select a menu option: ")

    if(mode == '1'):
        editStudentByBarcode()
    elif(mode == '2'):
        editStudentByName()
    elif(mode == '3'):
        mainMenu()
    else:
        editStudent()

def editStudentByBarcode():
    clearScreen()
    db = TinyDB('students.json')
    students = Query()
    scannedBarcode = raw_input("Barcode: ")
    scannedBarcodeNew = str(scannedBarcode[:1])

    try:
        db.get(students.barcode == "%s") % scannedBarcodeNew
    except IndexError:
        pass

    raw_input("Press Enter to continue...")
    mainMenu()

def editStudentByName():
    pass


def mainMenu():
    clearScreen()

    print("=== Main Menu ===")
    print("1: Take Attendance")
    print("2: Add Student")
    print("3: Edit Student")
    print("4: Remove Student")
    print("5: Print all barcodes")
    print("6: Exit")
    mode = raw_input("Select a menu option: ")

    if(mode == '1'):
        mainMenu()
    elif(mode == '2'):
        inputStudent()
    elif(mode == '3'):
        editStudent()
    elif(mode == '4'):
        mainMenu()
    elif(mode == '5'):
        printAllBarcodes()
    elif(mode == '6'):
        clearScreen()
        exit(0)
    else:
        print("Invalid option...")
        mainMenu()

mainMenu()