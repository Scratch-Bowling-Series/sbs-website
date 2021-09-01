



class Page:
    pagelinks = []
    pagestyles = []





def create_page_obj(current, per, total):
    if total == 0:
        return None
    next = current + 1
    prev = current - 1
    last = int(total / per)
    first = 1
    group = current / 6
    if group > int(group):
        group = int(group) + 1
    else:
        group = int(group)
        
    group *= 6

    if group < 6:
        group = 6



    group = int(group)

    pagelinks = [first, prev, group - 5, group - 4, group - 3, group - 2, group - 1, group, next, last]

    nextoff = ''
    prevoff = ''
    lastoff = ''
    firstoff = ''

    if current == first:
        firstoff = 'off'
        prevoff = 'off'

    if current == last:
        lastoff = 'off'
        nextoff = 'off'


    pagestyles = [firstoff, prevoff,
                    if_selected(group - 5, current, last),
                    if_selected(group - 4, current, last),
                    if_selected(group - 3, current, last),
                    if_selected(group - 2, current, last),
                    if_selected(group - 1, current, last),
                    if_selected(group, current, last),
                  nextoff, lastoff]

    page = Page()
    page.pagelinks = pagelinks
    page.pagestyles = pagestyles
    return page


def if_selected(value, current, last):
    if value == current:
        if value > last:
            return 'selected off'
        else:
            return 'selected'
    else:
        if value > last:
            return 'off'
        else:
            return ''