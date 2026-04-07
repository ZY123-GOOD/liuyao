def conclusion(divination,line,score):

    notes=[]

    if score>=4:

        result="吉"

    elif score>=1:

        result="中"

    else:

        result="凶"

    confidence=0.5+(score*0.06)

    confidence=max(0.2,min(0.9,confidence))

    return{

        "result":result,

        "confidence":round(confidence,2),

        "score":score,

        "notes":notes

    }