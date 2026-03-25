def moving_lines(lines):

    result=[]

    for l in lines:

        if l.moving:

            result.append(l.pos)

    return result