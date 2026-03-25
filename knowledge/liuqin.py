from knowledge.wuxing import relation

def get_relative(day_element,line_element):

    r = relation(day_element,line_element)

    if r=="same":
        return "兄弟"

    if r=="generate":
        return "子孙"

    if r=="generated_by":
        return "父母"

    if r=="control":
        return "妻财"

    if r=="controlled":
        return "官鬼"