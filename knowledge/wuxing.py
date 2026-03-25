GENERATE = {

"木":"火",
"火":"土",
"土":"金",
"金":"水",
"水":"木"

}

CONTROL = {

"木":"土",
"土":"水",
"水":"火",
"火":"金",
"金":"木"

}

def generates(a,b):

    return GENERATE.get(a)==b


def controls(a,b):

    return CONTROL.get(a)==b


def relation(a,b):

    if a==b:
        return "same"

    if generates(a,b):
        return "generate"

    if generates(b,a):
        return "generated_by"

    if controls(a,b):
        return "control"

    if controls(b,a):
        return "controlled"

    return "none"