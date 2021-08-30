



class Page:
    pagelinks = []
    pagestyles = []





def create_page_obj(current, per, total):
    next = current + 1
    prev = current - 1
    last = int(total / per)
    first = 1
    group = round(current / 6) + 1
    group *= 6

    if group < 6:
        group = 6

    if group > last + 6:
        group = last + 6

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
        if current > last:
            return 'selected off'
        else:
            return 'selected'
    else:
        if current > last:
            return 'off'
        else:
            return ''