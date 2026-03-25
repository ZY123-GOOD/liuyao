MAP={

"career":"官鬼",
"wealth":"妻财",
"exam":"父母",
"health":"官鬼",
"investment":"妻财"

}

def identify_use_god(intent,gender):

    if intent=="relationship":

        if gender=="male":

            return "妻财"

        return "官鬼"

    return MAP.get(intent)