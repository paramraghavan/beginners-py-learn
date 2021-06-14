pass_marks = 70

if pass_marks == 70:
    print('pass')


its_raining = True                  # you can change this to False

if its_raining:
    print("It's raining!")


its_raining = True                  # you can change this to False
its_not_raining = not its_raining   # False if its_raining, True otherwise

if its_raining:
    print("It's raining!")
if its_not_raining:
    print("It's not raining.")

if its_raining:
    print("It's raining!")
else:
    print("It's not raining.")

if pass_marks < 70:
    print('Retake Exam')
elif pass_marks == 70:
    print('Just Pass')
elif pass_marks == 80:
    print('Pass C grade')
elif pass_marks == 90:
    print('Pass B grade')
elif 90 <= pass_marks <= 95: # elif pass_marks >= 90 and pass_marks <= 95:
    print('Pass A grade')
else:
    print(f'Not sure what to do with pass marks: {pass_marks}')
