    """
    Открытие файла и удаление пустых строк
    """
    while True:
        a = input("Введите название файла: ")
        try:
            with open(a, 'r', encoding='utf-8') as file:
             lines = file.readlines()
            break
        except FileNotFoundError as er:
            print(er, " Неверное название файла Попробуйте снова")
    fixed_lines = [line for line in lines if line.strip()]
    return fixed_lines

def check (text: list) -> bool:
    """
    Функция проверки, правильно ли заполнены поля "пол"
    Если поле заполнено неправильно, выведет, его номер
    """
    genders = {"М", "м", "Мужской", "мужской", "Ж", "ж", "Женский", "женский"}
    num = 0
    Errnum = 0
    if len(text) %7 != 0:
        print("Файл повреждён, нарушена структура анкет")
        return False
    for i in range (3, len(text), 7):
            gender = text[i]
            num+=1
            try:
                gender = gender.split(": ", 1)[1].strip()
            except IndexError :
                Errnum+=1
                print(" Ошибка в формате антеты №", num)
                continue
            if gender not in genders:
                print ("В строке ", num, " Ошибка в записи пола\n")
                Errnum+=1
    if Errnum != 0:
        return False
    if Errnum == 0:
        print("\nВсе поля \"пол\" заполнены правильно \n")
    return True

def men() -> int:
    """
    Функция для поиска всех мужских анкет, записи их в новый файл
    """
    f = open ("new_data.txt", 'w', encoding='utf-8')
    cntr = 0
    text = fopen()
    is_valid = check(text)
    if not is_valid:
        f.close
        return
    for i in range (3, len(text), 7):
            gender_value = text[i].split(": ", 1)[1].strip()
            if gender_value in {"М", "м", "Мужской", "мужской"}:
                cntr+=1
                f.writelines([
                     text[i-3],
                     text[i-2],
                     text[i-1],
                     text[i],
                     text[i+1],
                     text[i+2],
                     text[i+3] + '\n',
                 ])
    f.close()
    return cntr
men()