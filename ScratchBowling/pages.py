



class Page:
    pagelinks = []
    pagestyles = []





def create_page_obj(current, per, total):
    next = current + 1
    prev = current - 1
    last = total / per
    first = 1
    group = round(current / 6) + 1
    group *= 6

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
                    if_selected(group - 5, current),
                    if_selected(group - 4, current),
                    if_selected(group - 3, current),
                    if_selected(group - 2, current),
                    if_selected(group - 1, current),
                    if_selected(group, current),
                  nextoff, lastoff]

    page = Page()
    page.pagelinks = pagelinks
    page.pagestyles = pagestyles
    return page


def if_selected(value, current):
    if value == current:
        return 'selected'
    else:
        return ''