from knowledge.wuxing import relation

def analyze_relation(use_god,shi):

    r = relation(use_god.element,shi.element)

    if r=="generate":

        return "support"

    if r=="control":

        return "pressure"

    if r=="controlled":

        return "blocked"

    return "normal"