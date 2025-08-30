print("-Grading as per Final Results-")
print("Enter subject name and marks - Type 'done' when finished aploding marks.\n")

total = 0
count = 0

while True:
    subject = input("Enter The Subject Name (or type 'done' to quit): ")
    if subject.lower() == "done":
        break
    
    marks = int(input("Enter marks in " + subject + ": "))
    
    # grade for each subject
    if marks >= 90:
        grade = "A"
    elif marks >= 80:
        grade = "B"
    elif marks >= 70:
        grade = "C"
    elif marks >= 60:
        grade = "D"
    else:
        grade = "F"
    
    print(subject, ":", marks, "-> Grade", grade, "\n")
    
    total += marks
    count += 1

# final grade
if count > 0:
    average = total / count
    if average >= 90:
        final_grade = "A"
    elif average >= 80:
        final_grade = "B"
    elif average >= 70:
        final_grade = "C"
    elif average >= 60:
        final_grade = "D"
    else:
        final_grade = "F"
    
    print(" Final Result")
    print("Total Marks:", total)
    print("Average:", average)
    print("Final Grade:", final_grade)
else:
    print("None of the subjects entered.")
