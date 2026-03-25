from knowledge.wuxing import generates,controls

def calc_strength(

element,
month_element,
day_element,
moving

):

    score=0

    if generates(month_element,element):

        score+=2

    if generates(day_element,element):

        score+=1

    if controls(month_element,element):

        score-=2

    if controls(day_element,element):

        score-=1

    if moving:

        score+=1

    return score